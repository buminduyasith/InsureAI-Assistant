from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from asyncio import sleep 
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

