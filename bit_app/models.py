import uuid, re
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

def validate_contact_number(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError("Enter a valid contact number.")


def validate_currency(value):
    if not re.match(r'^[A-Z]{3}$', value):
        raise ValidationError("Currency must be entered in the format: 'USD'.")

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length = 50, blank=False, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    primary_contact_number = models.CharField(max_length=15, blank=False, validators=[validate_contact_number])
    secondary_contact_number = models.CharField(max_length=15, blank=True, null=True, validators=[validate_contact_number])
    currency = models.CharField(max_length=3, blank=False, validators=[validate_currency])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Calendar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_ends_on = models.DateField()
    recurrence = models.CharField(max_length=10, choices=[('daily', 'daily'), ('weekly', 'weekly'), 
            ('monthly', 'monthly'), ('yearly', 'yearly')])

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError('End date must be after start date.')
        if self.start_time < datetime.date.today():
            raise ValidationError('Start date must be after current date')
        
