from pydantic import BaseModel

class UserAuth(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    token: str
