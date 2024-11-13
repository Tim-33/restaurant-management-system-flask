from pydantic import BaseModel

class HelloModel(BaseModel):
    id: int
    message: str