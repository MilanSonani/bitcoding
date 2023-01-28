from .serializers import UserRegisterSerializer, CalendarSerializer, CalendarResponseSerializer, UpdateMeetingSerializer, UserCalendarSerializer
from .models import CustomUser, Calendar
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .utils import get_location_by_ip

class UserRegistrationView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            username = serializer.data.get('username')
            date_of_birth = serializer.data.get('date_of_birth')
            primary_contact_number = serializer.data.get('primary_contact_number')
            secondary_contact_number = serializer.data.get('secondary_contact_number')
            currency = get_location_by_ip(request)
            
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.date_of_birth = date_of_birth
            user.primary_contact_number = primary_contact_number
            user.secondary_contact_number = secondary_contact_number
            user.currency = currency
            user.save()
            return Response({'status': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCalendarView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            calendar = Calendar.objects.filter(user=serializer.validated_data['user'], 
            start_time__lte=serializer.validated_data['end_time'], 
            end_time__gte=serializer.validated_data['start_time'])
            if calendar:
                return Response({"error": "User is not available in the provided date and time"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                calendar = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalendarDetailView(generics.RetrieveAPIView):
    parser_classes = [MultiPartParser]

    queryset = Calendar.objects.all()
    serializer_class = CalendarResponseSerializer


class UserCalendarDetailView(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = UserCalendarSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Calendar.objects.filter(user__id=user_id)


class DeleteMeetingView(APIView):
    parser_classes = [MultiPartParser]

    def delete(self, request, pk, format=None):
        meeting_obj = get_object_or_404(Calendar, pk=pk)
        meeting_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateMeetingView(APIView):
    parser_classes = [MultiPartParser]

    def put(self, request, pk, format=None):
        meeting_obj = get_object_or_404(Calendar, pk=pk)
        serializer = UpdateMeetingSerializer(meeting_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
