from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from asyncio import sleep
from Agent import init

app = FastAPI()


@app.get("/")
def read_root():
    data = init()
    print("data", data)
    return {"Hello": data}

