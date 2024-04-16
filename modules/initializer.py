from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class initialise:
    def __init__(self):
        self.allQues = []
        self.IMEI = 3849348779472
        self.module = "Recruitment"

        # MongoDB connection and other initialization logic
        client = MongoClient(os.getenv('CONNECTION_STRING'))
        database_name = os.getenv('DATABASE_NAME')
        collection_name = os.getenv('USER_COLLECTION')
        self.db = client[database_name]
        self.collection = self.db[collection_name]
        self.keyCollection = self.db[os.getenv('KEY_COLLECTION')]

        self.train_document = self.keyCollection.find_one({"type": 'train'})
        print('self.keyCollection:',self.keyCollection)

        if self.train_document is not None:
            self.mongo_train_key = self.train_document['train']
        else:
            print('Training data is not present')

        

init = initialise()