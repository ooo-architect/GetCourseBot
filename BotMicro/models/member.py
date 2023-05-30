from typing import Optional
from odetam.async_model import AsyncDetaModel


class Member(AsyncDetaModel):
    # key is GetCourse uid
    uid: str  # duplicate key for optimized queries
    name: str  # first + second name
    user_id: Optional[int]  # telegram user id
