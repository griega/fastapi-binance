import pydantic
import typing
from p_models.pair import Pair


class Courses(pydantic.BaseModel):
    exchange: typing.Optional[str]
    courses: typing.List[Pair]