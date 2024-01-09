from motor.core import AgnosticDatabase
from typing import Union

async def getIfUserExists(db: AgnosticDatabase, username: str) -> bool:

    try:
        usersInfo = await db.command("usersInfo")
        for user in usersInfo["users"]:
            if user["user"] == username:
                return True
    except Exception:
        pass

    return False

async def getUser(db: AgnosticDatabase, username: str) -> Union[dict, None]:
    userInfo = await db.command("usersInfo")
    for user in userInfo["users"]:
        if user["user"] == username:
            return user["user"]