#! /bin/env python3

import logging

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from datamodels import UserCreationForm
from responses import BASE_RESPONSE, CLIENT_RESPONSE, COLIS_RESPONSE, DELIVERY_RESPONSE, IS_USER_CONNECTED, VENDOR_RESPONSE
from typing import Union, Any

### We should be calling the external mongoDB driver to handle MongoDB-related requests
import mongoserv as mongo

### We configure the logging util
logging.basicConfig(filename="./livre-mon-colis.log", encoding="utf-8", level=logging.DEBUG)

app = FastAPI()


@app.get("/")
async def get():

    logging.debug("ROUTE: `/`")

    return JSONResponse(BASE_RESPONSE, status_code=200, headers={
        "application/type": "text/json"
    })

@app.get("/hello-world")
async def helloWorld():
    logging.debug("ROUTE: `/hello-world`")

    return JSONResponse({
        "content": await mongo.helloWorld()
    }, status_code=200, headers={
        "Content-Type": "application/json"
    })

### User Area
@app.get("/api/user/{username}")
async def getUser(username: str):
    logging.debug("ROUTE: `/api/user/\{username\}`")

    content = await mongo.getUser(username)
    print("User content:", content)

    return JSONResponse({
        "content": content
    }, status_code=200)

@app.post("/api/user/create/")
async def postUser(form: Request):

    logging.debug("ROUTE: `/api/user/create`")

    data = await form.json()
    print(f"Body: {data['username']}, {data['password']}, {data['roles']}")
    logging.info(f"Data Content: {data}")

    username, password, roles = data['username'], data['password'], data['roles']

    result = await mongo.createUser("users", username, password, roles)


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
@app.get("/api/colis/{package_id}")
async def getPackage(package_id: int):
    return JSONResponse(COLIS_RESPONSE)

@app.get("/api/delivery/id/{delivery_id}")
async def getDelivery(delivery_id: int):
    return JSONResponse(DELIVERY_RESPONSE)

@app.get("/api/delivery/name/{delivery_name}")
async def getReverseDelivery(delivery_name: str):
    return JSONResponse(DELIVERY_RESPONSE)

@app.get("/api/client/{client_id}")
async def getClient(client_id: int):
    return JSONResponse(CLIENT_RESPONSE)

@app.get("/api/vendors/{vendor_id}")
async def getVendor(vendor_id: int):
    return JSONResponse(VENDOR_RESPONSE)

### Test Area with websockets
@app.get("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.receive()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")