from typing import Union
from motor.core import AgnosticCollection, AgnosticDatabase

async def createCollection(database: AgnosticDatabase, collection_name: str) :
  return await database.create_collection(collection_name)

async def deleteCollection(database: AgnosticDatabase, collection_name: str) -> AgnosticCollection:
  """Delete one collection and all its content

  Args:
      client (AsyncIOMotorClient): The current MongoDB client
      database_name (str): The holding database name
      collection_name (str): The collection to delete

  Returns:
      AgnosticCollection: The deleted collection
  """
  return await database.drop_collection(collection_name)

async def insertIntoCollection(collection: AgnosticCollection, data: Union[dict, list]):
  if isinstance(data, list):
    collection.insert_many(data)
  else:
    collection.insert_one(data)

async def removeFromCollection(collection: AgnosticCollection, data_to_remove: Union[dict, list]):
  if isinstance(data_to_remove, list):
    collection.delete_many(data_to_remove)
  else:
    collection.delete_one(data_to_remove)

async def listCurrentCollections(database: AgnosticDatabase):
  collections = []
  for collection_name in await database.list_collection_names():
    collections.append(collection_name)

  print(", ".join(collections))