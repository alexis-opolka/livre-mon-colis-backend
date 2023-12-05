import os
import sys
import asyncio
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

async def pingServer():
    MONGODB_URI = os.environ['MONGODB_URI']

    try:
        client = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))
    except ValueError as ve:
        print("There is a value error: ", ve)


    try:
        await client.admin.command("ping")
        print("Pinged the deployment, successfully connected to MongoDB!")
        for db_info in await client.list_database_names():
            print(db_info)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    print("Started the Async Server")
    try:
        asyncio.run(pingServer())
    except KeyboardInterrupt:
        exit()