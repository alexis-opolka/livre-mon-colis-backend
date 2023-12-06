import os
import sys
import asyncio
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

if not DEBUG:
    MONGODB_URI = os.environ['MONGODB_URI']
else:
    MONGODB_URI = "mongodb://root:root@127.0.0.1/local"
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
        for db_info in await MONGO_CLIENT.list_database_names():
            print(db_info)
    except Exception as e:
        print(e)

async def getData():

    global MONGO_CLIENT

    try:
        await MONGO_CLIENT.admin
    except Exception as err:
        print("Issue here:", err)

if __name__ == "__main__":
    print("Started the Async Server, trying to access the MongoDB at the following address:", MONGODB_URI)
    try:
        asyncio.run(pingServer())
    except KeyboardInterrupt:
        exit()
