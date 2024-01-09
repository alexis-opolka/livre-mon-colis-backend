from motor.core import AgnosticCollection

from logs import log
from typing import Union

async def createDocument(collection: AgnosticCollection, document: dict):

    return await collection.insert_one(document)

async def updateDocument(collection: AgnosticCollection, document: dict, field_to_update: Union[str, int], value_to_update: any, operation: str):
    document = await collection.find_one(document)

    if document is not None:
        if isinstance(document[field_to_update], (list, tuple)):
            if operation == "insert":

                document.update({
                    field_to_update: document[field_to_update] + value_to_update
                })
            else:
                document[field_to_update] = value_to_update

        elif isinstance(document[field_to_update], dict):
            if operation == "insert":

                document.update({
                    field_to_update: document[field_to_update] + value_to_update
                })
            else:
                document.update({
                    field_to_update: value_to_update
                })
        
        else:
            ### In the case of a non-iterable value such as a str, int or float
            ### we're by default going to write on the last value
            document[field_to_update] = value_to_update

        log(f"[updateDocument]({operation}): {document}")


        collection.replace_one({
            "_id": document["_id"]
        }, document)