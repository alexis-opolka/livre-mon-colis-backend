import os
import asyncio
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

from typing import Union

from logs import log
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
    from .connections.setter.documents import (
        createDocument as __createDocument,
        updateDocument as __updateDocument
    )

    from .connections.getter.database import (
        getIfDatabaseExists as __getIfDatabaseExists,
        getDB as __getDB
    )
    from .connections.getter.users import (
        getIfUserExists as __getIfUserExists,
    )
    from .connections.getter.collections import (
        getIfCollectionExists as __getIfCollectionExists,
        getCollection as __getCollection,
        listCurrentCollections as __listCurrentCollections,
    )
    from .connections.getter.documents import (
        getIfUserDocumentExists as __getIfUserDocumentExists,
        getUserDocument as __getUserDocument,
        getIfDocumentExists as __getIfDocumentsExists,
        getDocument as __getDocument,
        getAllDocuments as __getAllDocuments
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
        getIfUserDocumentExists as __getIfUserDocumentExists,
        getUserDocument as __getUserDocument,
        getAllDocuments as __getAllDocuments,
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
        "password": user_pwd,
        "roles": user_roles 
    }

    ### Let's check if it already exists
    if not await __getIfUserDocumentExists(current_collection, user_data):
        ### If it doesn't exist, let's create the document

        await __createUserDocument(current_collection, user_data)

    ### Now that all our user-related work has been done,
    ### we can create a `glossary` of the related database
    ### for each user.
    if not await __getIfDatabaseExists(MONGO_CLIENT, "users"):
        _, db = await __createDB(MONGO_CLIENT, "users")
    else:
        db = await __getDB(MONGO_CLIENT, "users")
    
    if not await __getIfCollectionExists(db, "glossary"):
        glossary = await __createCollection(db, "glossary")
    else:
        glossary = await __getCollection(db, "glossary")

    
    user_glossary = {
        "username": username,
        "db": user_roles[0] if isinstance(user_roles, (list, tuple)) else user_roles
    }

    if not await __getIfDocumentsExists(glossary, user_glossary, "username"):
        await __createDocument(glossary, user_glossary)

    log(f"Should have the glossary for {username}!")

    return True


async def getUserDocument(username: str, password: str) -> Union[dict, None]:

    user_db = None

    if await __getIfDatabaseExists(MONGO_CLIENT, "users"):
        glossary_db = await __getDB(MONGO_CLIENT, "users")

        if await __getIfCollectionExists(glossary_db, "glossary"):
            glossary_collection = await __getCollection(glossary_db, "glossary")
        
            if await __getIfDocumentsExists(glossary_collection, {"username": username}, "username"):
                document = await __getDocument(glossary_collection, {"username": username}, "username")

                user_db = document["db"]

    if user_db is not None:

        db = await __getDB(MONGO_CLIENT, user_db)
        collection = await __getCollection(db, PRIVATE_USER_COLLECTION)

        user_data = await __getUserDocument(collection, username)

        if user_data["password"] == password:
            return user_data

    return None

async def getUserObjectId(username: str) -> Union[ObjectId, None]:
    user_object_id = None
    user_db = None

    if await __getIfDatabaseExists(MONGO_CLIENT, "users"):
        glossary_db = await __getDB(MONGO_CLIENT, "users")

        if await __getIfCollectionExists(glossary_db, "glossary"):
            glossary_collection = await __getCollection(glossary_db, "glossary")

            if await __getIfDocumentsExists(glossary_collection, {"username": username}, "username"):
                document = await __getDocument(glossary_collection, {"username": username}, "username")

                user_db = document["db"]

    if user_db is not None:
        db = await __getDB(MONGO_CLIENT, user_db)
        collection = await __getCollection(db, PRIVATE_USER_COLLECTION)

        user_data = await __getUserDocument(collection, username)


        if "_id" in user_data:
            user_object_id = user_data["_id"]

    return user_object_id


## Package Area

async def getPackage(package_id: int):
    result = {}

    if await __getIfDatabaseExists(MONGO_CLIENT, "packages"):
        db = await __getDB(MONGO_CLIENT, "packages")

        if await __getIfCollectionExists(db, "store"):
            collection = await __getCollection(db, "store")

            package = ObjectId(package_id)
            doc_filter = {
                "_id": package
            }

            log(f"[getPackage] (document filter) --> {doc_filter}")

            if await __getIfDocumentsExists(collection, doc_filter, "_id"):
                result = await __getDocument(collection, doc_filter, "_id")

    return result

### User-Defined Methods
### Seller Area
async def createPackage(seller: str, carrier: str, client: str):
    ### 1 - Get the seller ObjectId from its name
    ### 2 - Get the carrier ObjectId from its name
    ### 3 - Get the client ObjectId from its name

    seller_id = await getUserObjectId(seller)
    carrier_id = await getUserObjectId(carrier)
    client_id = await getUserObjectId(client)

    log(f"[New Package] - IDs (seller,carrier,client): {seller_id},{carrier_id},{client_id}")

    package_id = await __createPackage(seller_id, carrier_id, client_id)
    log(f"[New Package] - Package ID: {package_id}")

async def getPackagesFromSeller(seller_name: str):
    result = []

    if await __getIfDatabaseExists(MONGO_CLIENT, "packages"):
        db = await __getDB(MONGO_CLIENT, "packages")

        if await __getIfCollectionExists(db, "glossary"):
            collection = await __getCollection(db, "glossary")

            ### Let's get the User ObjectId
            user_objId = await getUserObjectId(seller_name)

            if await __getIfDocumentsExists(collection, {
                "seller": user_objId
            }, "seller"):
                result = await __getDocument(collection, {
                    "seller": user_objId
                }, "seller")

                log(f"[getPackagesFromSeller] (Packages) - {result['packages']}")

    return result['packages']

async def getUserDocumentFromId(user_id: str):
    result = {}

    if await __getIfDatabaseExists(MONGO_CLIENT, "users"):
        db = await __getDB(MONGO_CLIENT, "users")

        if await __getIfCollectionExists(db, "glossary"):
            glossary = await __getCollection(db, "glossary")

            doc_filter = {
                "_id": ObjectId(user_id)
            }

            log(f"[getUserDocumentFromId] (Result) --> {result}")

            if await __getIfDocumentsExists(glossary, doc_filter, "_id"):
                result = await __getDocument(glossary, doc_filter, "_id")

    log(f"[getUserDocumentFromId] (Result) --> {result}")

    return result

### Carrier Area
async def createParcelDelivery(vehicle: int, packages: Union[list, tuple]):
    ...

async def updateParcelDeliveryStatus(parcel_delivery_id: int, new_status: dict):
    ...

async def setPackageDeliveryStatus(package_id: int, status: str):
    ...

### Client Area
async def validatePackageDelivery(package_id: int):
    ...

### Internal methods
async def __createPackage(seller_id: ObjectId, carrier_id: ObjectId, client_id: ObjectId) -> ObjectId:
    ### 3 Dimensions: hauteur/largeur/longueur
    ### States: emballe/arrive/depart/livre/recu
    ### known facts:
    ###     - seller
    ###     - carrier
    ###     - client (name, address, zip-code, town, mail, phone)
    
    ### 1 - Create or get the PACKAGES_DB database inside MongDB
    ### 2 - Create or get the Collection
    ### 3 - Create the package document with all required data
    ### 4 - Somehow get the ObjectID and return it

    ### Create or get the PACKAGES_DB database
    if await __getIfDatabaseExists(MONGO_CLIENT, PACKAGES_DB):
        ### The database already exists
        db = await __getDB(MONGO_CLIENT, PACKAGES_DB)
    else:
        ### The database doesn't exists yet
        ### The `_` variable is the creation status (isn't used but should be remembered)
        _, db = await __createDB(MONGO_CLIENT, PACKAGES_DB)

    ### Create or get the Collection
    if not await __getIfCollectionExists(db, "store"):
        collection = await __createCollection(db, "store")
    else:
        collection = await __getCollection(db, "store")

    ### Create the package document
    package_document = {
        "weight": 0,
        "dimensions": {
            "height": 0,
            "width": 0,
            "lenght": 0
        },
        "state": {
            "wrapped": {
                "state": False,
                "timestamp": None,
            },
            "storage-arrival": {
                "state": False,
                "timestamp": None,
            },
            "storage-departure": {
                "state": False,
                "timestamp": None,
            },
            "delivery": {
                "state": False,
                "timestamp": None,
            },
            "received": {
                "state": False,
                "timestamp": None,
            }
        },
        "seller": seller_id,
        "carrier": carrier_id,
        "client": client_id
    }

    document = await __createDocument(collection, package_document)
    log(f"DOCUMENT INSERTED: {document.inserted_id}")

    ### Now that we created the document object and got its ObjectId
    ### We're going to build up the glossary and/or update the package entry

    if not await __getIfCollectionExists(db, "glossary"):
        glossary = await __createCollection(db, "glossary")
    else:
        glossary = await __getCollection(db, "glossary")

    glossary_package_document_search = {
        "seller": seller_id
    }

    glossary_package_document = {
        "seller": seller_id,
        "packages": [
            document.inserted_id
        ]
    }

    if not await __getIfDocumentsExists(glossary, glossary_package_document_search, "seller"):
        await __createDocument(glossary, glossary_package_document)
    else:
        await __updateDocument(glossary, glossary_package_document_search, "packages", [document.inserted_id], "insert")

    glossary = await __getDocument(glossary, glossary_package_document_search, "seller")

    if document is not None:
        return document.inserted_id

async def getAllCarriers() -> list:

    result = []

    if await __getIfDatabaseExists(MONGO_CLIENT, "carrier"):
        db = await __getDB(MONGO_CLIENT, "carrier")
        
        if await __getIfCollectionExists(db, PRIVATE_USER_COLLECTION):
            collection = await __getCollection(db, PRIVATE_USER_COLLECTION)

            documents = await __getAllDocuments(collection)

            if documents != []:
                for doc in documents:
                    log(f"[getAllCarriers](doc-looping) - DOC: {doc}")
                    result.append(doc["username"])

    log(f"[getAllCarriers] --> {result}")


    return result

async def getAllClients() -> list:

    result = []

    if await __getIfDatabaseExists(MONGO_CLIENT, "client"):
        db = await __getDB(MONGO_CLIENT, "client")
        
        if await __getIfCollectionExists(db, PRIVATE_USER_COLLECTION):
            collection = await __getCollection(db, PRIVATE_USER_COLLECTION)

            documents = await __getAllDocuments(collection)

            if documents != []:
                for doc in documents:
                    log(f"[getAllClients](doc-looping) - DOC: {doc}")
                    result.append(doc["username"])

    log(f"[getAllClients] --> {result}")


    return result
    

PACKAGES_DB = "packages"


if __name__ == "__main__":
    os.system("cls")
    print("Started the Async Server, trying to access the MongoDB at the following address:", MONGODB_URI)
    try:
        asyncio.run(getUserDocument("test", "test"))
    except KeyboardInterrupt:
        exit()
