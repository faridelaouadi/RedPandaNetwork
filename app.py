import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
from werkzeug.utils import secure_filename
import os
import time
from async_predict import *
import asyncio

import requests
import json

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return redirect(url_for("home"))

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route('/home')
def home():
    return render_template("dashboard.html",user=session["user"], value="home")

def isRedPanda(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join('./static/', f"uploads/{filename}")
    file.save(filepath)
    #inclding the latest iteration which is pretty accurate
    url = "https://redpandaclassifier.cognitiveservices.azure.com/customvision/v3.0/Prediction/22689ca4-d96e-414f-8e9a-b913f7626f15/classify/iterations/Iteration3/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'de5c1effa9b9486b8ea2fd665faf461a'}
    r =requests.post(url,data=open(filepath,"rb"),headers=headers)
    response = r.json()
    predictions = response['predictions']
    #the predictions always come in the format of "prediction first" so predictions[i] is what the classifier preidcted
    if predictions[0]['tagName'][0] == "-":
        #not panda
        return False
    else:
        return True

@app.route('/upload', methods=["GET","POST"])
def upload():
    message = ''
    true_positives = 0
    total_images = 0
    false_positives = 0
    if request.method == 'POST':
        camera_ID = request.form.get('camera_ID')
        uploaded_files = request.files.getlist("file")
        total_images = len(uploaded_files)
        filepaths = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join('./static/', f"uploads/{filename}")
            file.save(filepath)
            filepaths.append(filepath)
        
        results = asyncio.run(main(filepaths))
        #NOTE TO SELF --- THE PRICING TIER YOU ARE ON IN CUSTOMVISION.AI HAS A LIMIT OF 10 CALLS A SECOND!!!

        message = "Batch Report"
        true_positives=int((results.count(True)/total_images)*100)
        false_positives = 100 - true_positives

        #upload to blob storage 
        #add entry to database 
        #clear uploads folder so server is always optimised

    return render_template("upload_pics.html",message=message,true_positives=true_positives,false_positives=false_positives,  total_images=total_images, user=session["user"], value="upload")

@app.route('/viewPics')
def viewPics():
    return render_template("view_pics.html",user=session["user"], value="view")


@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("index"))

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

if __name__ == "__main__":
    app.run(debug=True)

