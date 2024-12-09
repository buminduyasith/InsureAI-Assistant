from fastapi import FastAPI
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


@app.get("/chat")
def read_root():
    data = init()
    return {"payload": data}

