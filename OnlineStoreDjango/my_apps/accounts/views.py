import os
import requests

from django.shortcuts import render, redirect
import google_auth_oauthlib.flow


def log(request):
    logs = []
    with open("information.log") as log_file:
        for line in log_file:
            logs.append(line)
    return render(request, "accounts/logs.html", {"logs": logs[::-1]})


def google_login(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                # "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            }
        },
        scopes=["https://www.googleapis.com/auth/userinfo.email"],
    )

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    BASE_URL = os.getenv("BASE_URL")
    print("redirect_uri:", f"{BASE_URL}auth/ok")
    flow.redirect_uri = f"{BASE_URL}auth/ok"

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    return redirect(authorization_url)


def ok(request):
    state = request.GET.get("state")
    code = request.GET.get("code")
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            }
        },
        scopes=None,
        state=state,
    )
    BASE_URL = os.getenv("BASE_URL")
    flow.redirect_uri = f"{BASE_URL}auth/ok"
    flow.fetch_token(code=code)

    credentials = flow.credentials
    credentials = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    print(credentials)
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    response = requests.get(GOOGLE_USER_INFO_URL, params={"access_token": credentials["token"]})
    response_dict = response.json()
    return render(request, "oauth/ok.html", {"detail": response_dict["email"]})
