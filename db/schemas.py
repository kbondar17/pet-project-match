from datetime import datetime
from typing import Optional, Any

from pydantic import AnyUrl, BaseModel, validator


class Model(BaseModel):
    uid: int

    class Config:
        orm_mode = True


class User(Model):
    name: Optional[str]

    gender = Optional[str]
    prog_lang = Optional[str]

    self_description = Optional[str]
    project_description = Optional[str]

    was_shown_to = Optional[str]
    has_seen = Optional[str]
    profile_pic = Optional[str]
    tag = Optional[str]


    class Config:
        arbitrary_types_allowed = True
