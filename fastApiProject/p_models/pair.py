import pydantic


class Pair(pydantic.BaseModel):
    direction: str
    value: float