from datetime import datetime
from rest_framework import serializers
from .models import CustomUser, Calendar
from .utils import validate_meeting

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=16)
    email = serializers.EmailField(required=True)
    date_of_birth = serializers.DateField(input_formats=["%m-%d-%Y"])
    primary_contact_number = serializers.CharField(max_length=15, required=True)
    secondary_contact_number = serializers.CharField(max_length=15, required=False)
    currency = serializers.CharField(default='USD')

    def validate(self, data):
        email = data.get('email', None)
        password = data.get("password", None)
        if not email and not password:
            raise serializers.ValidationError({"Error": "Email or password is missing."})
        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

    def validate_recurrence(self, value):
        if value not in ['daily', 'weekly', 'monthly', 'yearly']:
            raise serializers.ValidationError("Invalid recurrence value. Accepted values are 'daily', 'weekly', 'monthly', 'yearly'")
        return value

    def validate(self, data):
        date_time_obj = datetime.strptime(str(data['start_time'].replace(tzinfo=None)), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(str(data['end_time'].replace(tzinfo=None)), '%Y-%m-%d %H:%M:%S').time()
        end_date_time_obj = datetime.strptime(str(data['meeting_ends_on']), '%Y-%m-%d')

        if date_time_obj > datetime.strptime(str(data['end_time'].replace(tzinfo=None)), '%Y-%m-%d %H:%M:%S'):
            raise serializers.ValidationError(f"Meetnig end time must be greter than start time")
        
        availability, start_time_x, end_time_x = validate_meeting(date_time_obj.date(),
            end_date_time_obj.date(),
            date_time_obj.time(),
            end_time, 
            data['recurrence'], 
            data['user']
        )
        if availability:
            raise serializers.ValidationError(f"User is not available between {start_time_x} to {end_time_x} ")
        return data


class CalendarResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ('user', 'title', 'start_time','end_time', 'meeting_ends_on', 'recurrence')


class UserCalendarSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id')
    class Meta:
        model = Calendar
        fields = ('id', 'user_id', 'title', 'start_time', 'end_time', 'meeting_ends_on', 'recurrence')


class UpdateMeetingSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    meeting_ends_on = serializers.DateTimeField(required=False)
    recurrence = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.title = validated_data.get('title', instance.title)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.meeting_ends_on = validated_data.get('meeting_ends_on', instance.meeting_ends_on)
        instance.recurrence = validated_data.get('recurrence', instance.recurrence)
        instance.save()
        return instance

    def validate(self, data):
        date_time_obj = datetime.strptime(str(data['start_time'].replace(tzinfo=None)), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(str(data['end_time'].replace(tzinfo=None)), '%Y-%m-%d %H:%M:%S').time()
        end_date_time_obj = datetime.strptime(str(data['meeting_ends_on'].replace(tzinfo=None)), '%Y-%m-%d %H:%M:%S')
        availability, start_time_x, end_time_x = validate_meeting(date_time_obj.date(),
            end_date_time_obj.date(),
            date_time_obj.time(),
            end_time, 
            data['recurrence'], 
            data['user_id']
        )
        if availability:
            raise serializers.ValidationError(f"User is not available between {start_time_x} to {end_time_x} ")
        return data
