from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
# the file should be avaiable at base directory (IE: Working Directory)
CLIENT_SECRETS_FILE = "credentials.json"
RED_URL =  'http://127.0.0.1:8000/rest/v1/calendar/redirect'

if os.name=='posix':
    CLIENT_SECRETS_FILE = "/etc/secrets/credentials.json"
    RED_URL =  'https://gcal-event-basic.onrender.com/rest/v1/calendar/redirect'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection and REDIRECT URL.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile','openid']


@api_view(['GET'])
def GoogleCalendarInitView(request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = RED_URL

    auth_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    request.session['state'] = state

    return Response({"auth_url": auth_url})


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = request.session['state']
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = RED_URL

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    auth_response = request.get_full_path()
    flow.fetch_token(authorization_response=auth_response)

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    # Check if credentials are in session
    if 'credentials' not in request.session:
        return redirect('/rest/v1/calendar/init')

    # Load credentials from the session.
    credentials = Credentials(**request.session['credentials'])

    service = build('calendar', 'v3', credentials=credentials)
    # get list of cal
    calendar_list = service.calendarList().list().execute()
    # event list
    resp_event = []
    # since a user has multiple cals, iterate to each
    # using their IDs
    for cal_no in calendar_list['items']:
        events  = service.events().list(calendarId=cal_no['id']).execute()
        # if the cal has events, extend our resp list
        if events['items']:
            resp_event.extend(events['items'])
    # if no events found, return No events
    if len(resp_event) == 0:
        return Response({"message": "User has no events in Calendar"})
    return Response({"event_list": resp_event})

    
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
        }
