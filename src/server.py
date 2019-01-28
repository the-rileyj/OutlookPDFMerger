# from flask import jsonify
from flask import Flask, jsonify, redirect, request, session
from requests_oauthlib import OAuth2Session

import json
import pyperclip
import requests


app = Flask(__name__)

# @app.route('/')
# def send_js(path):
#     return send_from_directory('html', path)

app_id = "440e01e0-294d-402b-a3e9-c8749e34cf31"
scopes = "Mail.Read Mail.ReadWrite".split(" ")
redirect_url= "http://localhost/callback"

secret = "ypNUF9642+ratvxYOEQ1[+^"
token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
# graph_url = 'https://graph.microsoft.com/v1.0'

app.secret_key = secret

@app.route("/auth")
def auth():
    aad_auth = OAuth2Session(app_id,
    scope=scopes,
    redirect_uri=redirect_url
    )

    sign_in_url, state = aad_auth.authorization_url("https://login.microsoftonline.com/common/oauth2/v2.0/authorize", prompt='login')

    session['auth_state'] = state

    return redirect(sign_in_url, code=301)


@app.route("/callback")
def callback():
    resp = requests.post(token_url, data={
        "client_id":app_id,
        "client_secret":secret,
        "code": request.args.get("code"),
        "redirect_uri": redirect_url,
        "grant_type": "authorization_code"
    })

    print(resp.text)

    token = json.loads(resp.text)["access_token"]

    # user = get_user(token)

    pyperclip.copy(token)

    # session['user'] = {
    #     'is_authenticated': True,
    #     'name': user['displayName'],
    #     'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName']
    # }

    session["oauth_token"] = token

    return redirect("/", code=301)


@app.route("/")
def index():
    return "WOW"


# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")

# def get_user(token):
#   graph_client = OAuth2Session(token=token)
#   # Send GET to /me
#   user = graph_client.get('{0}/me'.format(graph_url))
#   # Return the JSON result
#   return user.json()


if __name__ == "__main__":
    app.run(port=80)
