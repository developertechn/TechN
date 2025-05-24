from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://developertechn:Navneet%4040441@cluster0.wjhivc7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def register_user(name, email,mobile, password):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['TechN']
    collection = db['users']
    
    user_data = {
        'name': name,
        'email': email,
        'mobile': mobile,
        'password': password
    }
    
    result = collection.insert_one(user_data)
    return result.inserted_id