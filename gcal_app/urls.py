from django.urls import path
from . import views
from os import environ

# Set this env var so local testing doesnt raise errors
environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

urlpatterns = [
    path('rest/v1/calendar/init/', views.GoogleCalendarInitView, name='g_ouauth'),
    path('rest/v1/calendar/redirect/', views.GoogleCalendarRedirectView, name='g_red_cal')
]
