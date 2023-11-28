from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from config import Config
import json

class WorkflowService:

    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME


    def get_workflow_list(self, user_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        agency_json_list = []
        agency_json = {
                'workflow_id' : 1,
                'workflow_name' : "G2PDeep", 
            }
        agency_json_list.append(agency_json)
        agency_json = {
                'workflow_id' : 2,
                'workflow_name' : "PGen", 
            }
        agency_json_list.append(agency_json)
        agency_json = {
                'workflow_id' : 3,
                'workflow_name' : "RNASeq", 
            }
        agency_json_list.append(agency_json)
        #json_output = json.dumps(agency_json_list)
        #print(json_output)
        session.close()
        return agency_json_list
    
