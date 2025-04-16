from pydantic import BaseModel

class SearchQuery(BaseModel):
    prompt: str
    schema: str
