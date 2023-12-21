from motor.core import AgnosticDatabase


async def createUser(db: AgnosticDatabase, username: str, user_pwd: str, user_roles: list):
    db.command({
        "createUser": username,
        "pwd": user_pwd,
        "roles": user_roles
    })