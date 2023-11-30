from flask import Flask, session, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import os
from pytz import timezone
import json
import uuid


app = Flask(__name__)
CORS(app)
# app.config.from_object("config.DevelopmentConfig")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ app.config['DB_USERNAME'] + ':' + app.config['DB_PASSWORD'] + '@' + app.config['DB_CONFIG'] + '/' + app.config['DATABASE_NAME']

if __name__ == "__main__":
	app.run()


        

@app.route('/execute_as', methods=['POST'])
def upload_workflow():
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

    # Unzip the uploaded file
    unzip_directory = os.path.join(staging_location, 'unzipped')
    if not os.path.exists(unzip_directory):
        os.makedirs(unzip_directory)
    
    import zipfile
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_directory)

    # Execute the execute.sh shell file
    unzip_directory = os.path.join(unzip_directory, file.filename[:-4])
    print(unzip_directory)
    execute_sh_path = os.path.join(unzip_directory, 'execute.sh')
    print(execute_sh_path)
    if os.path.exists(execute_sh_path):
        os.system(f'chmod +x {execute_sh_path}')
        os.system(execute_sh_path)
        output_file = file_path = os.path.join(staging_location, "output.log")
        try:
            with open(output_file, 'r') as file:
                file_contents = file.read()
                print("File contents:", file_contents)
        except FileNotFoundError:
            print(f"File not found at {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")
        return json.dumps({'response': "Workflow uploaded and executed successfully", "output_log": file_contents}), 200
    else:
        return json.dumps({'response': "execute.sh not found in the uploaded file"}), 400











    


    

