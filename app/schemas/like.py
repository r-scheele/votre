from pydantic import BaseModel
from pydantic.types import conint


class LikeSchema(BaseModel):
    post_id: int
    dir: conint(le=1)
