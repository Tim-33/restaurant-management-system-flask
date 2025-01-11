from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CustomBase(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    disabled: bool = False