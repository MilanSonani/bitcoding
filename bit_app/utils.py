import pytz
from datetime import datetime 
import pycountry
from geopy.geocoders import Nominatim
from dateutil.relativedelta import relativedelta
from .models import Calendar
from django.conf import settings
from django.utils import timezone


def get_location_by_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)
    location = geolocator.geocode(ip)
    get_contry_name = geolocator.reverse(location.raw['lat']+","+location.raw['lon'])
    try:
        address = get_contry_name.raw['address']['country']
        country = pycountry.countries.get(name=address)
        currency = pycountry.currencies.get(numeric=country.numeric)
    except:
        currency.alpha_3 = 'INR'
    return currency.alpha_3


def validate_meeting(start_date, end_date, start_time, end_time, recurrence, user):
    date_list = []
    while True:
        if start_date <= end_date:
            date_list.append({
                "start_date" : datetime.combine(start_date, start_time), 
                "end_date" : datetime.combine(start_date, end_time)
            })
        else:
            break
        
        if recurrence == 'weekly':
            start_date = start_date + relativedelta(weeks=1)
        if recurrence == 'monthly':
            start_date = start_date + relativedelta(months=1)
        if recurrence == 'yearly':
            start_date = start_date + relativedelta(years=1)
        if recurrence == 'daily':
            start_date = start_date + relativedelta(days=1)

    user_mettings = Calendar.objects.filter(
        user=user,
        meeting_ends_on__gte=datetime.today()
    )
    for metting in user_mettings:
        recurrence = metting.recurrence
        start_date = metting.start_time
        metting_list=[]
        
        while True:
            default_timezone = pytz.timezone(settings.TIME_ZONE)

            if start_date > default_timezone.localize(datetime.combine(metting.meeting_ends_on, start_date.time())):
                break
            if start_date >= timezone.now():
                metting_list.append({
                    "start_date": datetime.combine(start_date.date(), start_date.time()),
                    "end_date": datetime.combine(start_date.date(), metting.end_time.time())
                })

            if recurrence == 'weekly':
                start_date = start_date + relativedelta(weeks=1)
            if recurrence == 'monthly':
                start_date = start_date + relativedelta(months=1)
            if recurrence == 'yearly':
                start_date = start_date + relativedelta(years=1)
            if recurrence == 'daily':
                start_date = start_date + relativedelta(days=1)

        for i in metting_list:
            for j in date_list:
                if (i['start_date'] >= j['start_date'] and i['start_date'] < j['end_date']) \
                or (i['end_date'] > j['start_date'] and i['end_date'] <= j['end_date']) \
                or (i['start_date'] < j['end_date'] and i['end_date'] > j['start_date']):
                    return True, j["start_date"], j["end_date"]
    
    return False, None, None
