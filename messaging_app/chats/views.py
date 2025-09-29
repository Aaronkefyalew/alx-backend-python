from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from rest_framework.decorators import action
from django.http import Http404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    # Add filtering by participant
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Custom action to get all messages for a specific conversation
        """
        conversation_id = pk
        try:
            conversation = self.get_object()
            # Check if user is participant of the conversation
            if not IsParticipantOfConversation().has_object_permission(request, self, conversation):
                return Response({"detail": "You do not have permission to access these messages."}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            # Filter messages by conversation_id
            messages = Message.objects.filter(conversation_id=conversation_id)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            raise Http404("Conversation not found")


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['sender__email', 'message_body']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Override get_queryset to filter messages by conversation_id if provided
        """
        queryset = super().get_queryset()
        conversation_id = self.request.query_params.get('conversation_id')
        
        if conversation_id:
            # Filter messages by conversation_id and check permissions
            messages = Message.objects.filter(conversation_id=conversation_id)
            # Verify user has permission to access this conversation's messages
            if messages.exists():
                conversation = messages.first().conversation
                if not IsParticipantOfConversation().has_object_permission(self.request, self, conversation):
                    return Message.objects.none()
            return messages
        return queryset

    def destroy(self, request, *args, **kwargs):
        """
        Override delete to check if user has permission to delete the message
        """
        try:
            instance = self.get_object()
            # Check if user is participant of the conversation
            if not IsParticipantOfConversation().has_object_permission(request, self, instance.conversation):
                return Response({"detail": "You do not have permission to delete this message."}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            return super().destroy(request, *args, **kwargs)
            
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, 
                          status=status.HTTP_404_NOT_FOUND)
