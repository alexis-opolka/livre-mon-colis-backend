from motor.core import AgnosticDatabase, AgnosticCollection

async def createUser(db: AgnosticDatabase, username: str, user_pwd: str, user_roles: list):

    database_roles = []

    for role in user_roles:
        if role in ["user"]:
            database_roles.append("read")
        elif role in ["admin"]:
            database_roles.append("readWrite")

    db.command({
        "createUser": username,
        "pwd": user_pwd,
        "roles": database_roles
    })


async def createUserDocument(user_collection: AgnosticCollection, user_document: dict):

    return await user_collection.insert_one(user_document)

async def deleteUser(db: AgnosticDatabase, username: str) -> bool:
    db.command({
        "dropUser": username
    })