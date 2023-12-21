import os
import sys
import asyncio
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

from connections.setter.database import createDB, deleteDB
from connections.setter.collections import createCollection, insertIntoCollection, listCurrentCollections
from connections.setter.users import createUser

load_dotenv()

DEBUG = True

if not DEBUG:
    MONGODB_URI = os.environ['MONGODB_URI']
else:
    MONGODB_URI = "mongodb://127.0.0.1/admin"
MONGO_CLIENT = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))

async def establish_env():
    global MONGO_CLIENT
    global MONGODB_URI

    if MONGO_CLIENT is not None:
        os.environ['MONGO_CLIENT'] = MONGO_CLIENT
    else:
        os.environ['MONGO_CLIENT'] = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))

async def pingServer():
    global MONGO_CLIENT

    try:
        await MONGO_CLIENT.admin.command("ping")
        print("Pinged the deployment, successfully connected to MongoDB!")

        available_db = []
        print("Are available to the user, the following databases:", end=" ")
        for db_info in await MONGO_CLIENT.list_database_names():
            available_db.append(db_info)

        print(", ".join(available_db) + ".")
    except Exception as e:
        print(e)

async def getData():

    global MONGO_CLIENT

    try:
        await MONGO_CLIENT.admin.command()
    except Exception as err:
        print("Issue here:", err)

async def mainScript():
    test_db = "test-all"
    await pingServer()
    f_db = await createDB(MONGO_CLIENT, test_db)
    print("The result of the creation is:", f_db)
    print("The result of the deletion is:", await deleteDB(MONGO_CLIENT, test_db))

    creation_status, db = await createDB(MONGO_CLIENT, test_db)
    test_collection = await createCollection(db, "users")
    await insertIntoCollection(test_collection, {
        "name": "test-user",
        "pwd": "test",
        "roles": []
    })
    await listCurrentCollections(db)
    await createUser(db, "test-user", "test", [])

if __name__ == "__main__":
    os.system("cls")
    print("Started the Async Server, trying to access the MongoDB at the following address:", MONGODB_URI)
    try:
        asyncio.run(mainScript())
    except KeyboardInterrupt:
        exit()
