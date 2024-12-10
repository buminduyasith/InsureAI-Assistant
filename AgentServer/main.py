from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import StreamingResponse, JSONResponse
from asyncio import sleep
from insurance_assistant import init
from fastapi.middleware.cors import CORSMiddleware
import os

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
    data = await request.json()  
    message = data.get("message")
    payload = init(message)
    return {"payload": payload}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        filename = os.path.join("uploads", file.filename)
        
        with open(filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return JSONResponse(content={
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(content),
            "status": "uploaded successfully"
        })
    
    except Exception as e:
        return JSONResponse(
            content={
                "error": str(e),
                "status": "upload failed"
            }, 
            status_code=500
        )