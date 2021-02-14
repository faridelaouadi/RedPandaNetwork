import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
from werkzeug.utils import secure_filename
import os
import time
import asyncio
import json
from async_predict_local import *
from blob import *

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

def break_up_filepaths(filepaths,divisor):
    number_of_lists = ( len(filepaths) // divisor ) + 1# 11//5 = 2
    list_of_lists = []
    counter = 0
    for i in range(number_of_lists):
        sub_list = filepaths[counter:counter+divisor]
        list_of_lists.append(sub_list)
        counter += divisor
    return list_of_lists

panda_files = []
non_panda_files = []
camera_ID = ''

def get_modified_lists(panda_files,non_panda_files,changes):
    dictionary_of_changes = {item:changes.count(item) % 2 for item in changes} #something like {'p_0': 2, 'np_0': 1}
    modified_panda_files = []
    modified_non_panda_files = []
    for i in range(len(panda_files)):
        try:
            if dictionary_of_changes[f"p_{i}"] == 1:
                modified_non_panda_files.append(panda_files[i])
            else:
                modified_panda_files.append(panda_files[i])
        except:
            #there is no key for that image
            modified_panda_files.append(panda_files[i])
    
    for i in range(len(non_panda_files)):
        try:
            if dictionary_of_changes[f"np_{i}"] == 1:
                modified_panda_files.append(non_panda_files[i])
            else:
                modified_non_panda_files.append(non_panda_files[i])
        except:
            #there is no key for that image
            modified_non_panda_files.append(non_panda_files[i])
    
    return modified_panda_files,modified_non_panda_files

def clear_uploads_folder():
    filelist = [ f for f in os.listdir('./static/uploads/')]
    for f in filelist:
        os.remove(os.path.join('./static/uploads/', f))

@app.route('/upload_analysed_images/', methods=['POST'])
def upload_analysed_images():
    if request.method == "POST":
        global panda_files
        global non_panda_files
        global camera_ID
        changes = request.get_json()

        modified_panda_files,modified_non_panda_files = get_modified_lists(panda_files,non_panda_files,changes)
        
    #at this point we have the perfectly classified images for panda and not panda  
    # 
    # reset both file lists so we dont mess up the other function          
    panda_files = []
    non_panda_files = [] 

    for non_panda in modified_non_panda_files:
        extension = non_panda[0][1:].split('.')[1]
        image_name = f'non_panda_{uuid.uuid1()}.{extension}'
        filepath = non_panda[0]
        upload_image_to_container(camera_ID,image_name,filepath)
        upload_image_to_container("non-pandas",image_name,filepath)
    
    for panda in modified_panda_files:
        extension = panda[0][1:].split('.')[1] #getting the extension of the image e.g PNG, JPEG etc 
        image_name = f'panda_{uuid.uuid1()}.{extension}'
        filepath = panda[0]
        upload_image_to_container(camera_ID,image_name,filepath)
        upload_image_to_container("pandas",image_name,filepath)
    
    clear_uploads_folder()

    #TODO ----
    #get back the blob link 
    #insert row into database for the panda and non panda images

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/upload', methods=["GET","POST"])
def upload():
    message = ''
    true_positives = 0
    total_images = 0
    false_positives = 0
    global panda_files
    global non_panda_files
    global camera_ID
    labels = model_setup()
    if request.method == 'POST':
        camera_ID = request.form.get('cameraID')
        uploaded_files = request.files.getlist("file")
        total_images = len(uploaded_files)
        filepaths = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join('./static/', f"uploads/{filename}")
            file.save(filepath)
            filepaths.append(filepath)
        
        '''
        # the 5 lines below this are for using the external API
        results = []
        list_of_lists = break_up_filepaths(filepaths,4) #break up the filepaths into groups of 4
        for filepaths in list_of_lists:
            results = results + asyncio.run(main(filepaths))
            time.sleep(2) #wait 2 seconds before another call'''
        
        '''
        #using local model with async
        results = []
        labels = model_setup()
        for filepath in filepaths:
            if classify_non_async(filepath, labels) == 'panda':
                results.append(True)'''

        #using async model
        results = asyncio.run(main(filepaths,labels)) #this is a list of (imageFile,Boolean)
        

        for (imageFile,classification,confidence) in results:
            if classification == True: #it is a panda
                panda_files.append([imageFile,confidence])
            else:
                non_panda_files.append([imageFile,confidence])

        message = "Batch Report"
        true_positives=int((len(panda_files)/total_images)*100)
        false_positives = 100 - true_positives

    return render_template("upload_pics.html",message=message,true_positives=true_positives,false_positives=false_positives,panda_files=panda_files,non_panda_files=non_panda_files,total_images=total_images, user=session["user"], value="upload")

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

