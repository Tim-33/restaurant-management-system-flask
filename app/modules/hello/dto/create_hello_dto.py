from pydantic import BaseModel

class CreateHelloDto(BaseModel):
    message: str