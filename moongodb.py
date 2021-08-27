from pymongo import MongoClient

class Connect(object):
    @staticmethod    
    def get_connection(username,password,db):
        return MongoClient(f"mongodb+srv://{username}:{password}@cluster0.ztfid.mongodb.net/{db}?retryWrites=true&w=majority")

