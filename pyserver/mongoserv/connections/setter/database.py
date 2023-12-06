import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, Async
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

async def create(client: AsyncIOMotorClient, database_name: str) -> bool:
  client.admin
