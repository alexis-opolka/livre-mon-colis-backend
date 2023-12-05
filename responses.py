from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['user_shopping_list']

# Get the database
dbname = get_database()

BASE_RESPONSE = {
    "status": 200,
    "content": "Hello World, I'm the Backend for Livre Mon Colis"
}

### User Area
IS_USER_CONNECTED = {
    "status": 200,
    "content": ""
}