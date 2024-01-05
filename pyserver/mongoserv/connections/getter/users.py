from motor.core import AgnosticDatabase

async def getIfUserExists(db: AgnosticDatabase, username: str) -> bool:
    usersInfo = await db.command("usersInfo")
    for user in usersInfo["users"]:
        if user["user"] == username:
            return True
        
    return False