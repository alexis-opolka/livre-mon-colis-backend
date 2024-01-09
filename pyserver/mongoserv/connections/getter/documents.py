from motor.core import AgnosticCollection
from typing import Union

async def getIfDocumentExists(collection: AgnosticCollection, document: dict, tag_to_check: str) -> bool:

    try:
        found_document = await collection.find(document).limit(1).to_list(1)

        if found_document[0][tag_to_check] == document[tag_to_check]:
            return True

    except IndexError:
        pass

    return False

async def getDocument(collection: AgnosticCollection, document: dict, tag_to_check: str) -> Union[dict, None]:

    found_document = await collection.find(document).limit(1).to_list(1)

    print("--->", found_document)

    if found_document[0][tag_to_check] == document[tag_to_check]:
        return found_document[0]
    else:
        return None

async def getAllDocuments(collection: AgnosticCollection) -> list[dict]:
   cursor = collection.find({})

   result = []

   for document in await cursor.to_list(1000):
    result.append(document)

    return result

### User-Area
async def getIfUserDocumentExists(collection: AgnosticCollection, document: dict) -> bool:
    mongo_filter =  {
        "username": document["username"]
    }

    try:
        found_document = await collection.find(mongo_filter).limit(1).to_list(1)

        if found_document[0]["username"] == document["username"]:
            print("FOUND")
            return True
    except IndexError:
        pass

    print("NOT FOUND")
    return False

async def getUserDocument(collection: AgnosticCollection, username: str) -> Union[dict, None]:
    mongo_filter =  {
        "username": username
    }

    try:

        found_document = await collection.find(mongo_filter).limit(1).to_list(1)
        print("USER DOCUMENT:", found_document)

        if found_document[0]["username"] == username:
            return found_document[0]
        
    except IndexError:
        return None