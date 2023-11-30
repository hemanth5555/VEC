from flask import Flask, session, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import os
from pytz import timezone
import json
from services.login_service import LoginService
from services.agency_service import WorkflowService
from services.user_service import UserService
import uuid


app = Flask(__name__)
CORS(app)
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ app.config['DB_USERNAME'] + ':' + app.config['DB_PASSWORD'] + '@' + app.config['DB_CONFIG'] + '/' + app.config['DATABASE_NAME']

if __name__ == "__main__":
    print("Started")
    app.run()

'''
    Initiating database connection with SQLAlchemy
'''
db = SQLAlchemy(app)


'''
    session dictionary
'''
sessions = {}

cluster_info = {0:["VEC_VEN1", "VEC_VEN3"], 1: ["VEC_VEN4"], 2: ["VEC_VEN4"], 3: ["VEC_VEN5"]}
final_cluster = 3
ven_info = {"VEC_VEN1": "http://54.80.26.203:7001/execute_as", "VEC_VEN2": "http://54.242.250.88:7001/execute_as", "VEC_VEN3":"http://44.204.23.120:7001/execute_as", "VEC_VEN4":"http://52.73.70.189:7001/execute_as", "VEC_VEN5":"http://3.88.66.66:7001/execute_as"}
workflow_reqs = {"RAM": 16, "Storage": "24", "CUPS": 2, "Type": "Compute"}

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



'''
    Rest end points to authenticate the user
'''
@app.route('/login', methods=['POST'])
def do_login():
    login_details = request.get_json(force=True)
    username = login_details['username']
    password = login_details['password']
    login_service = LoginService()
    user = login_service.get_user_info(username)
    passwd = login_service.get_encrypted_password(password)
    print(passwd)
    print(password)
    if(user.user_password == passwd):
        print("Creating session for user " + username)
        session_token = str(uuid.uuid4())
        sessions[session_token] = str(user.user_id)
        print(session_token)
        print(username)
        return json.dumps({'response': {"session_token" : session_token, "username": username}}), 200
    else:
        return json.dumps({'response': "Incorrect Credentials"}), 401
    

'''
    Rest end points to authenticate the user
'''
@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user_maintenance():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    user_service = UserService()
    if request.method == 'GET':
        print("Getting the list of users")
        response = user_service.get_user_list()
        return json.dumps({'response': response}), 200 
    
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            print("Creating user")
            name = data.get('user_name')
            password = data.get('user_password')
            first_name = data.get('user_firstname')
            last_name = data.get('user_lastname')
            print(name)
            print(password)
            print(first_name)
            print(last_name)
            return user_service.add_user(name, password, first_name, last_name)
        else:
            return "Invalid JSON data in the request body", 400
        
    elif request.method == 'DELETE':
        user_id = request.args.get('user_id')
        if user_id:
            print("Deleting user")
            return user_service.delete_user(int(user_id))
        else:
            return "Invalid JSON data in the request body", 400
        

'''
    Rest end points to upload the workflow
'''
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

    print(workflow_name)
    print(workflow_reqs)

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

    print("File processed successfulluy!")
    print("Cluster Info", cluster_info)

    # url = "http://3.88.66.66:7001/execute_as"

    # Set the path to the file you want to attach
    file_path = file_path
    import requests

    # Set the form data including the file
    form_data = {
        'workflow_name': 'YourWorkflowName',
    }

    files = {'file': ('zipcon.zip', open(file_path, 'rb'))}

    
    print("Sending the file to cluster ", final_cluster)

    url = ven_info[cluster_info[final_cluster][0]]
    print("Cluster choosen for execution : ",cluster_info[final_cluster])
    print("Node choosen for execution : ", ven_info[cluster_info[final_cluster][0]])

    url = ven_info[cluster_info[final_cluster][0]]

    # Make the POST request
    try:
        response = requests.post(url, data=form_data, files=files)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        print("Request successful:", response.text)
        return json.dumps({'response': "Workflow uploaded successfully and execution initiated"}), 200
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return json.dumps({'response': f"Error in executing workflow: "}), 500
    


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







'''
    Rest API to get the list of workflows in the system
'''
@app.route('/workflows', methods=['GET', 'POST', 'DELETE'])
def get_workflows():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    generic_service = WorkflowService()
    if request.method == 'GET':
        print("Getting the workflow list")
        response = generic_service.get_workflow_list(int(user_id))
        return json.dumps({'response': response}), 200 



    


    

