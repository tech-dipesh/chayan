from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Chayan")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"Server is running"}

@app.post("/query")
def query(request: QueryRequest):
  print("Server is running")
  if not request.question:
    raise HTTPException(status_code=400, detail="Please Enter Something")
  return { f'{request.question}' }