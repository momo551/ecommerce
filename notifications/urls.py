from django.urls import path
from .views import ChatAPI

urlpatterns = [
    path('chat-api/', ChatAPI.as_view(), name='chat-api'),
]
