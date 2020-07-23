from pydantic import BaseModel
import enum
from fastapi import Query


class Role(str, enum.Enum):
    admin:str = "admin"
    personel:str = "personel"

class User(BaseModel):
    name: str
    password: str
    mail: str
    role: Role