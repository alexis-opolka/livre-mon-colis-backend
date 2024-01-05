from hashlib import sha256
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

from typing import Union

from .connections.setter.database import (
    createDB as __createDB,
    deleteDB as __deleteDB
)
from .connections.setter.collections import (
    createCollection as __createCollection,
    insertIntoCollection as __insertIntoCollection,
)
from .connections.setter.users import (
    createUser as __createUser,
    createUserDocument as __createUserDocument,
    deleteUser as __deleteUser
)

from .connections.getter.database import (
    getIfDatabaseExists as __getIfDatabaseExists,
    getDB as __getDB
)
from .connections.getter.users import (
    getIfUserExists as __getIfUserExists
)
from .connections.getter.collections import (
    getIfCollectionExists as __getIfCollectionExists,
    getCollection as __getCollection,
    listCurrentCollections as __listCurrentCollections
)
from .connections.getter.documents import (
    getIfDocumentExists as __getIfDocumentExists
)


load_dotenv()

DEBUG = True

if not DEBUG:
    MONGODB_URI = os.environ['MONGODB_URI']
else:
    MONGODB_URI = "mongodb://127.0.0.1/admin"
MONGO_CLIENT = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))

async def establish_env():
    global MONGO_CLIENT
    global MONGODB_URI

    if MONGO_CLIENT is not None:
        os.environ['MONGO_CLIENT'] = MONGO_CLIENT
    else:
        os.environ['MONGO_CLIENT'] = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))

async def pingServer():
    global MONGO_CLIENT

    try:
        await MONGO_CLIENT.admin.command("ping")
        print("Pinged the deployment, successfully connected to MongoDB!")

        available_db = []
        print("Are available to the user, the following databases:", end=" ")
        for db_info in await MONGO_CLIENT.list_database_names():
            available_db.append(db_info)

        print(", ".join(available_db) + ".")

        return available_db
    except Exception as e:
        print(e)

async def getData():

    global MONGO_CLIENT

    try:
        await MONGO_CLIENT.admin.command()
    except Exception as err:
        print("Issue here:", err)

async def mainScript():
    test_db = "test-all"
    await pingServer()
    f_db = await __createDB(MONGO_CLIENT, test_db)
    print("The result of the creation is:", f_db)
    print("The result of the deletion is:", await __deleteDB(MONGO_CLIENT, test_db))

    creation_status, db = await __createDB(MONGO_CLIENT, test_db)
    test_collection = await __createCollection(db, "users")
    await __insertIntoCollection(test_collection, {
        "name": "test-user",
        "pwd": "test",
        "roles": []
    })
    await __listCurrentCollections(db)
    await createUser(db, "test-user", "test", [])

async def helloWorld():
    term_size_x, term_size_y = os.get_terminal_size()
    print(term_size_x*"-")
    print("--- MongoDB Python Driver for `Livre Mon Colis Backend` ---")
    print(term_size_x*"-", end="\n\n")
    return await pingServer()


### User-Area

async def createUser(database_name: str, username: str, user_pwd: str, user_roles: Union[list, tuple, str], encrypted: bool = False) -> bool:

    ### Development ONLY
    DEBUG = True

    ### To create a user in mongoDB, we need to
    ###     - create the `database` where it will be created
    ###     - create the user inside this database
    ###     - create a specific `__users__` collection
    ###     - create a user-specific document entry in the  `__users__` collection

    private_users_collection = "__users__"

    if await __getIfDatabaseExists(MONGO_CLIENT, database_name):
        ### The database already exists
        db = await __getDB(MONGO_CLIENT, database_name)
    else:
        ### The database doesn't exists yet
        ### The `_` variable is the creation status (isn't used but should be remembered)
        _, db = await __createDB(MONGO_CLIENT, database_name)

    if isinstance(user_roles, str):
        ### If the user roles is only one as a string,
        ### let's wrap it inside a list as the private
        ### __createUser function handles only iterables (lists, tuples)
        user_roles = [user_roles]

    ### Let's create the User
    if not await __getIfUserExists(db, username):
        await __createUser(db, username, user_pwd, user_roles)
    else:
        if DEBUG:
            await __deleteUser(db, username)
        else:
            ### An early return because it doesn't make sense to continue
            ### the steps to create a user entry if it already exists
            return False
    
    ### Let's create the `__users__` collection
    if not await __getIfCollectionExists(db, private_users_collection):
        current_collection = await __createCollection(db, private_users_collection)
    else:
        current_collection = await __getCollection(db, private_users_collection)


    ### Let's create the user-specific document
    user_data = {
        "username": username,
        ### We're encrypting the password if it's not already the case
        "password": user_pwd if encrypted else sha256(user_pwd.encode("utf-8")).hexdigest(),
        "roles": user_roles
    }

    ### Let's check if it already exists
    if not await __getIfDocumentExists(current_collection, user_data):
        ### If it doesn't exist, let's create the document

        await __createUserDocument(current_collection, user_data)

    return True



if __name__ == "__main__":
    os.system("cls")
    print("Started the Async Server, trying to access the MongoDB at the following address:", MONGODB_URI)
    try:
        asyncio.run(mainScript())
    except KeyboardInterrupt:
        exit()
