from rest_framework import serializers
from .models import User, Conversation, Message


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email')  # Display sender's email
    sent_at = serializers.SerializerMethodField()  # Add a method field for customization

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def get_sent_at(self, obj):
        """Format the sent_at timestamp."""
        return obj.sent_at.strftime('%Y-%m-%d %H:%M:%S')


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)  # Include user details for participants
    messages = MessageSerializer(many=True, read_only=True)  # Include messages in the conversation
    total_messages = serializers.SerializerMethodField()  # Add a method field for the message count

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'total_messages']

    def get_total_messages(self, obj):
        """Calculate the total number of messages in the conversation."""
        return obj.messages.count()

    def validate_participants(self, value):
        """Ensure there are at least two participants in a conversation."""
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value
