# Google Calendar Events using Django

Fetch Events from Google Cal

An implementation of accessing events of Google Calendar using google-auth library and Django Framework.

These are the endpoints:

- /rest/v1/calendar/init/ -> GoogleCalendarInitView()

  Return Auth URL to which you can iniate a google authorization

- /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()

  Handles the redirect after login, and return the calendar list of the user

Steps to Create Credential files:

- Head to https://console.cloud.google.com/ and create a new app
- Enable Calendar API under API & Services -> Enabled APIs & Services
- Next, Create credentail - OAuth client id. Select web application as type, and under Authorized JavaScript origins add: http://127.0.0.1:8000/ and for Authorized redirect URIs: http://127.0.0.1:8000/rest/v1/calendar/redirect/ and click create.
- Download the file and save it as credential.json in the WD.
- Next go to OAuth consent Screen, click publish app and publish the app.

Note: A lot of code has been used as it is from ref. 2 with comments

References:

1. [https://developers.google.com/calendar/api/quickstart/python](https://developers.google.com/calendar/api/quickstart/python)
2. [https://developers.google.com/identity/protocols/oauth2/web-server](https://developers.google.com/identity/protocols/oauth2/web-server)
3. [https://developers.google.com/calendar/api/v3/reference/](https://developers.google.com/calendar/api/v3/reference/)
4. [https://developers.google.com/identity/openid-connect/openid-connect#python](https://developers.google.com/identity/openid-connect/openid-connect#python)
