from flask import Flask, request
from flask_cors import CORS  # Import CORS
from flask_bcrypt import Bcrypt
import json
from config import ApplicationConfig
from services.login_service import LoginService
from config import ApplicationConfig
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# Session(app)

app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)  # Configure CORS first


'''
    session dictionary
'''
sessions = {}


'''
    Check if the session token sent by client is valid and return the username for the session token
'''
def is_authenticated(session_token):
    print(session_token)
    print(sessions)
    if session_token in sessions:
        print("Logged in as - " + sessions[session_token])
        return sessions[session_token]
    raise Exception("Unauthorized request")


@app.route('/is_authenticated', methods=['GET'])
def is_user_authenticated():
    session_token = request.headers.get('session-token')
    if session_token in sessions:
        return json.dumps({'response': True}), 200
    else:
        return json.dumps({'response': False}), 401
    


@app.route('/login', methods=['POST'])
def do_login():
    # Your login logic here
    login_details = request.get_json(force=True)
    username = login_details['username']
    password = login_details['password']

    # AWS_REGION = os.getenv("password" + username[4])
    pw = os.getenv("password" + username[4])

    print(password)
    if(password == pw):
        print("Creating session for user " + username)
        session_token = str(uuid.uuid4())
        sessions[session_token] = str(username)
        print(session_token)
        print(username)
        return json.dumps({'response': {"session_token" : session_token, "username": username}}), 200
    else:
        return json.dumps({'response': "Incorrect Credentials"}), 401
    

@app.route('/upload_workflow', methods=['POST'])
def upload_workflow():
    # Check if the POST request has the 'workflow_name' field
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    
    if 'workflow_name' not in request.form:
        return json.dumps({'response': "Missing 'workflow_name' field"}), 400

    workflow_name = request.form['workflow_name']

    # Check if the POST request has the file part
    if 'file' not in request.files:
        return json.dumps({'response': "No file part"}), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return json.dumps({'response': "No selected file"}), 400
    
    staging_location = os.getenv("staging")
    print("File will be saved to staging location " + staging_location)
    if not os.path.exists(staging_location):
        os.makedirs(staging_location)
    
    file_path = os.path.join(staging_location, file.filename)
    file.save(file_path)
    print(file.filename)

    # # Save the file to a designated folder
    # file.save(os.path.join("path/to/your/upload/folder", file.filename))

    # Add your additional workflow processing logic here

    return json.dumps({'response': "Workflow uploaded successfully"}), 200
    

'''
    Rest end points to logout the authenticated user
'''
@app.route('/logout', methods=['POST'])
def do_logout():
    global sessions
    session_token = request.headers.get('session-token')
    print("Deleting session for user " +  sessions[session_token])   
    del sessions[session_token]
    return json.dumps({'response': 'success'}), 200


if __name__ == "__main__":
    app.run(port=7001)
