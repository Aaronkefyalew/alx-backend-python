from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Create an instance of DefaultRouter
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
