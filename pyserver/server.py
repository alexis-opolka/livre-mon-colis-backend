#! /bin/env python3

from bson import ObjectId
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from responses import BASE_RESPONSE, CLIENT_RESPONSE, COLIS_RESPONSE, DELIVERY_RESPONSE, IS_USER_CONNECTED, VENDOR_RESPONSE
from typing import Union

### We should be calling the external mongoDB driver to handle MongoDB-related requests
import mongoserv as mongo
from logs import logGETRoute, logPOSTRoute, log, warn, error

app = FastAPI()

@app.get("/")
async def get():

    logGETRoute("/")

    return JSONResponse(BASE_RESPONSE, status_code=200, headers={
        "application/type": "text/json"
    })

@app.get("/hello-world")
async def helloWorld():
    logGETRoute("/hello-world")

    return JSONResponse({
        "content": await mongo.helloWorld()
    }, status_code=200, headers={
        "Content-Type": "application/json"
    })

### User Area
@app.get("/api/user/{username}")
async def getUser(username: str):
    logGETRoute("/api/user/{username}")

    content = await mongo.getUser(username)
    print("User content:", content)

    return JSONResponse({
        "content": content
    }, status_code=200)

@app.post("/api/user/login/")
async def postUserLogin(form: Request):

    logPOSTRoute("/api/user/login/")

    data = await form.json()
    log(f"User {data['username']} trying to connect...")
    user_data = await mongo.getUserDocument(data["username"], data["password"])

    if user_data is not None:
        user_role = user_data["roles"]
        is_connected = True
    else:
        is_connected = False,
        user_role = None

    if is_connected:
        log(f"User {data['username']} connected!")
    else:
        log(f"User {data['username']} could not be authenticated!")

    return JSONResponse({
        "loggedIn": is_connected,
        "role": user_role,
    })

@app.post("/api/user/create/")
async def postUser(form: Request):

    logPOSTRoute("/api/user/create")

    data = await form.json()
    print(f"Body: {data['username']}, {data['password']}, {data['roles']}")
    log(f"Data Content: {data}")

    username, password, roles = data['username'], data['password'], data['roles']

    result = await mongo.createUser(roles, username, password, roles)


    if result is True:
        return JSONResponse({
            "status": 200,
            "content": f"User `{username}` has been created!"
        })
    else:
        return JSONResponse({
            "status": 500,
            "content": "Oospie Doopsie, something went wrong!"
        })

### Packages
@app.get("/api/package/{package_id}")
async def getPackage(package_id: str):
    logGETRoute("/api/package/{package_id}")

    result: dict = await mongo.getPackage(package_id)

    for key, value in result.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)

    log(f"[ROUTE: /api/package/:{package_id}][getPackage] (Serializable) --> {result}")


    log(f"[ROUTE: /api/package/:{package_id}][getPackage] (Result) --> {result}")

    return JSONResponse({
        "content": result
    }, status_code=200)



@app.post("/api/package/new/")
async def postNewPackage(form: Request):
    logPOSTRoute("/api/package/new/")

    data = await form.json()
    log(f"[PACKAGE](New) - {data}")

    seller, carrier, client = data["seller"], data["carrier"], data["client"]

    result = await mongo.createPackage(seller, carrier, client)

    return JSONResponse({
        "content": result
    }, status_code=200)

@app.get("/api/package/all/by-seller")
async def getPackagesBySeller(username: str):
    logGETRoute("/api/package/all/by-seller")

    result: list[ObjectId] = [str(package) for package in await mongo.getPackagesFromSeller(username)]
    log(f"[ROUTE: /api/package/all/by-seller:{username}][getPackagesBySeller] (Serializable Result) --> {result}")

    return JSONResponse({
        "content": result
    }, status_code=200)

@app.get("/api/carrier/list")
async def getCarrierList():
    logGETRoute("/api/carrier/list")

    result = await mongo.getAllCarriers()

    return JSONResponse({
        "content": result,
    }, status_code=200)

@app.get("/api/carrier/name/{carrier_id}")
async def getCarrierName(carrier_id: str):
    logGETRoute("/api/carrier/name/{carrier_id}")

    result = await mongo.getUserDocumentFromId(carrier_id)

    return JSONResponse({
        "content": result["username"]
    }, status_code=200)

@app.get("/api/client/name/{client_id}")
async def getClientName(client_id: str):
    logGETRoute("/api/client/name/{client_id}")

    result = await mongo.getUserDocumentFromId(client_id)

    return JSONResponse({
        "content": result["username"]
    }, status_code=200)

@app.get("/api/client/list")
async def getClientList():

    logGETRoute("/api/client/list")

    result = await mongo.getAllClients()

    return JSONResponse({
        "content": result,
    }, status_code=200)

@app.get("/api/seller/name/{seller_id}")
async def getSellerName(seller_id: str):
    logGETRoute("/api/seller/name/{seller_id}")

    result = await mongo.getUserDocumentFromId(seller_id)

    log(f"[ROUTE: /api/seller/name:{seller_id}][getSellerName] (Result) --> {result}")

    return JSONResponse({
        "content": result["username"]
    }, status_code=200)