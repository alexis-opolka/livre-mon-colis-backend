from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase

async def getIfDatabaseExists(client: AsyncIOMotorClient, database_name: str) -> bool:
    if database_name in await client.list_database_names():
        return True
    else:
        return False
    
async def getDB(client: AsyncIOMotorClient, database_name: str) -> AgnosticDatabase:
    supposed_db = client.get_database(database_name)

    if isinstance(supposed_db, AgnosticDatabase):
        return supposed_db