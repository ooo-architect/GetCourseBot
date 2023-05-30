from typing import Optional
from urllib.parse import quote

from odetam.async_model import AsyncDetaModel
from pydantic import Field, validator


# TODO: bag fix - key is quoted but queries executed with unquoted domain
class Account(AsyncDetaModel):
    # key is GetCourse account domain
    domain: str  # duplicate key
    groups: list[str] = Field(default_factory=list)  # groups GIDs

    @validator('key', pre=True, always=True)
    def set_key(cls, key: Optional[str]) -> Optional[str]:
        return quote(key) if key else None
