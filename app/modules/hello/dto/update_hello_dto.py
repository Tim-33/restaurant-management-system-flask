from pydantic import BaseModel

class UpdateHelloDto(BaseModel):
    message: str