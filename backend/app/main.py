from fastapi import FastAPI, Request
from agent import run_agent
from schemas import SearchQuery
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
async def search(query: SearchQuery):
    results = await run_agent(query.prompt, query.schema)
    return {"results": results}
