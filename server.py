from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

from responses import BASE_RESPONSE, IS_USER_CONNECTED

app = FastAPI()


@app.get("/")
async def get():
    return JSONResponse(BASE_RESPONSE)

### User Area
@app.get("/user")
async def get():
    return JSONResponse(IS_USER_CONNECTED)


### Test Area with websockets
@app.get("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.receive()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")