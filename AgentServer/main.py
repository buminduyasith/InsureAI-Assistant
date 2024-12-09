from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from asyncio import sleep
from Agent import init
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()  # Parse the JSON body
    message = data.get("message")  # Extract the message from the body
    payload = init(message)
    return {"payload": payload}

