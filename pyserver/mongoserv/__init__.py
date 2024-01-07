from hashlib import sha256
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

from typing import Union

### -----------------------------------------------------------
###
###  As I did not found a way to dynamically import the modules
###  from the called working directory and its type (i.e. main script, module)
###  I block the relative imports to two types, the `__main__` call
###  and the module call.
###
###  - For the module call (i.e. __name__ == `mongoserv`), we use the built-in
###    Python feature of file-system local import using the `from .module import *` expression.
###
###  - For the main call (i.e. __name__ == `__main__`), we use the built-in, most generic way,
###    of importing modules with the `from module import *` expression.
###
### -----------------------------------------------------------


if __name__ == "mongoserv":

    ### We're running the script as a module from another file (i.e. calling mongoserv/__init__.py)

    from .connections.setter.database import (
        createDB as __createDB,
        deleteDB as __deleteDB,
    )
    from .connections.setter.collections import (
        createCollection as __createCollection,
        insertIntoCollection as __insertIntoCollection,
    )
    from .connections.setter.users import (
        createUser as __createUser,
        createUserDocument as __createUserDocument,
        deleteUser as __deleteUser,
    )

    from .connections.getter.database import (
        getIfDatabaseExists as __getIfDatabaseExists,
        getDB as __getDB
    )
    from .connections.getter.users import (
        getIfUserExists as __getIfUserExists,
        getUser as __getUser,
    )
    from .connections.getter.collections import (
        getIfCollectionExists as __getIfCollectionExists,
        getCollection as __getCollection,
        listCurrentCollections as __listCurrentCollections,
    )
    from .connections.getter.documents import (
        getIfDocumentExists as __getIfDocumentExists,
    )

elif __name__ == "__main__":

    ### We're running the script as the main python file

    from connections.setter.database import (
        createDB as __createDB,
        deleteDB as __deleteDB
    )
    from connections.setter.collections import (
        createCollection as __createCollection,
        insertIntoCollection as __insertIntoCollection,
    )
    from connections.setter.users import (
        createUser as __createUser,
        createUserDocument as __createUserDocument,
        deleteUser as __deleteUser
    )

    from connections.getter.database import (
        getIfDatabaseExists as __getIfDatabaseExists,
        getDB as __getDB
    )
    from connections.getter.users import (
        getIfUserExists as __getIfUserExists
    )
    from connections.getter.collections import (
        getIfCollectionExists as __getIfCollectionExists,
        getCollection as __getCollection,
        listCurrentCollections as __listCurrentCollections
    )
    from connections.getter.documents import (
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

PRIVATE_USER_COLLECTION = "__users__"

async def createUser(database_name: str, username: str, user_pwd: str, user_roles: Union[list, tuple, str], encrypted: bool = False, key: str = None, iv: str = None) -> bool:

    ### Development ONLY
    DEBUG = True


    if DEBUG:
        print(os.get_terminal_size()[0]*"-")
        print("USER PASSWORD:", user_pwd, "ENCRYPTED ?", encrypted, "KEY:", key)
        print(os.get_terminal_size()[0]*"-")

    ### To create a user in mongoDB, we need to
    ###     - create the `database` where it will be created
    ###     - create the user inside this database
    ###     - create a specific `__users__` collection
    ###     - create a user-specific document entry in the  `__users__` collection

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
    if not await __getIfCollectionExists(db, PRIVATE_USER_COLLECTION):
        current_collection = await __createCollection(db, PRIVATE_USER_COLLECTION)
    else:
        current_collection = await __getCollection(db, PRIVATE_USER_COLLECTION)


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


async def getUser(username: str) -> dict:

    db = await __getDB(MONGO_CLIENT, PRIVATE_USER_COLLECTION)

    if await __getIfUserExists(db, username):
        user_data = await __getUser(db, username)
        print("USER DATA:", user_data)
    else:
        user_data = None

    return user_data




if __name__ == "__main__":
    os.system("cls")
    print("Started the Async Server, trying to access the MongoDB at the following address:", MONGODB_URI)
    try:
        asyncio.run(createUser("users", "test", "198,135,141,225,104,62,52,94,159,155,249,91,172,190,53,77,254,217,241,142,160,47,128,204,24,179,180,194,253,172,178,3,199,15,200,228,187,253,7,212,213,243,129,219,29,59,80,52", "user", True, "o5J1WshqJOCVqIJa5t3DLaM7J7BPuNYIgiwMrTliHWo"))
    except KeyboardInterrupt:
        exit()
