from django.urls import path
from .views import UserRegistrationView, CreateCalendarView, CalendarDetailView, UpdateMeetingView, DeleteMeetingView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('create/meeting/', CreateCalendarView.as_view(), name='create-meeting'),
    path('detail/meeting/<int:pk>', CalendarDetailView.as_view(), name='detail-meeting'),
    path('update/meeting/<int:pk>', UpdateMeetingView.as_view(), name='update-meeting'),
    path('delete/meeting/<int:pk>', DeleteMeetingView.as_view(), name='delete-meeting'),
]