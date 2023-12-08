from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

from responses import BASE_RESPONSE, CLIENT_RESPONSE, COLIS_RESPONSE, DELIVERY_RESPONSE, IS_USER_CONNECTED, VENDOR_RESPONSE

app = FastAPI()


@app.get("/")
async def get():
    return JSONResponse(BASE_RESPONSE)

### User Area
@app.get("/api/user/{user_id}")
async def getUser(user_id: int):
    return JSONResponse(IS_USER_CONNECTED)

### Packages
@app.get("/api/colis/{package_id}")
async def getPackage(package_id: int):
    return JSONResponse(COLIS_RESPONSE)

@app.get("/api/delivery/{delivery_id}")
async def getDelivery(delivery_id: int):
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