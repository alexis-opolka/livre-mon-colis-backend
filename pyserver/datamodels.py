from pydantic import BaseModel
from typing import Union

class UserCreationForm(BaseModel):
    username: str | None = None
    password: str | None = None
    roles: str | None = None 