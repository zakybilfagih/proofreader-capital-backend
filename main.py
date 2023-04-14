from fastapi import FastAPI
from pydantic import BaseModel
from proofreader import proofreader_v3


class MessagesReq(BaseModel):
    messages: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Capital Letter"}

@app.post("/proofreader/")
async def proofreader_capital(req: MessagesReq):
    result = proofreader_v3(req.messages)

    return {
        "result": result,
    }