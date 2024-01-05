from motor.core import AgnosticCollection

async def getIfDocumentExists(collection: AgnosticCollection, document: dict) -> bool:
    mongo_filter =  {
        "username": document["username"]
    }

    found_document = await collection.find(mongo_filter).limit(1).to_list(1)

    if found_document[0]["username"] == document["username"]:
        print("FOUND")
        return True
    
    print("NOT FOUND")
    return False