from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from proofreader import proofreader_v3

class MessagesReq(BaseModel):
    messages: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Capital Letter"}

@app.post("/capitalization_error_correction/")
async def proofreader_capital(req: MessagesReq):
    result = proofreader_v3(req.messages)

    return {
        "result": result,
    }
