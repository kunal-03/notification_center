from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class MessageBase(BaseModel):
    #sender: int
    receivers: List[int]
    message_content: Optional[str]
    context: Optional[str]

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    # timestamp: datetime
    # seen: bool
    # deleted: bool
    # archived: bool
    pass
