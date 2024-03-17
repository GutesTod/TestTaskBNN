from pydantic import BaseModel

class SumRequest(BaseModel):
    array: list[int]