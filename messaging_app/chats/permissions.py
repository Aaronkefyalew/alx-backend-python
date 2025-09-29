from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in obj.participants.all()
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
