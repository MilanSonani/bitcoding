from uuid import UUID
from django.urls import path
from .views import UserRegistrationView, CreateCalendarView, CalendarDetailView, \
                UserCalendarDetailView, UpdateMeetingView, DeleteMeetingView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('create/meeting/', CreateCalendarView.as_view(), name='create-meeting'),
    path('detail/meeting/<int:pk>', CalendarDetailView.as_view(), name='detail-meeting'),
    path('detail/user-meeting/<str:user_id>/', UserCalendarDetailView.as_view({'get': 'list'}), name='detail-user-meeting'),
    path('update/meeting/<int:pk>', UpdateMeetingView.as_view(), name='update-meeting'),
    path('delete/meeting/<int:pk>', DeleteMeetingView.as_view(), name='delete-meeting'),
]