
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.query import run_query
import subprocess

app = FastAPI(title='TalentMatch RAG - Demo')

class IngestRequest(BaseModel):
    run_ingest: bool = True

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

@app.post('/ingest')
async def ingest(req: IngestRequest):
    try:
        r = subprocess.run(['python', 'src/ingest.py'], check=True, capture_output=True, text=True)
        return {'status': 'ok', 'output': r.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e.stderr))

@app.post('/query')
async def query(req: QueryRequest):
    res = run_query(req.query, top_k=req.top_k)
    return res

@app.get('/health')
async def health():
    return {'status': 'healthy'}
