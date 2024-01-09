from motor.core import AgnosticCollection, AgnosticDatabase

async def getIfCollectionExists(db: AgnosticDatabase, collection_name: str) -> bool:
    for collection_id in await db.list_collection_names():
       if collection_id == collection_name:
          return True
    
    return False


async def listCurrentCollections(database: AgnosticDatabase) -> None:
  collections = []
  for collection_name in await database.list_collection_names():
    collections.append(collection_name)

  print(", ".join(collections))

async def getCollection(database: AgnosticDatabase, collection_name: str) -> AgnosticCollection:
   collection = database.get_collection(collection_name)

   return collection