from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    # List all notifications for the authenticated user
    path('notifications/', NotificationListView.as_view(), name='notifications'),

    # Mark a specific notification as read
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]