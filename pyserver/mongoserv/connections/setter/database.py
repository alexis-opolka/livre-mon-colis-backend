from typing import Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase
from dotenv import load_dotenv

load_dotenv()

async def createDB(client: AsyncIOMotorClient, database_name: str) -> Tuple[bool, AgnosticDatabase]:

  old_db = []
  for db_name in await client.list_database_names():
    old_db.append(db_name)

  if database_name in old_db:
    return ValueError("The database name already exists")

  db: AgnosticDatabase = client[database_name]
  await db.create_collection("empty-collection")

  new_db = []
  for db_info in await client.list_database_names():
    new_db.append(db_info)

  print("The new DB are:", ", ".join(new_db) + ".")

  for collection in await db.list_collection_names():
    print("[DB Check] Collection:", collection)

  return (old_db != new_db, db)

async def deleteDB(client: AsyncIOMotorClient, database_name: str) -> bool:

  current_db = []
  for db_name  in await client.list_database_names():
    current_db.append(db_name)

  if database_name not in current_db:
    return ValueError("The database name already exists")

  await client.drop_database(database_name)

  now_state = []

  for db_info in await client.list_database_names():
    now_state.append(db_info)

  return current_db != now_state
