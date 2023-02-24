from typing import List
from pydantic import BaseModel


class Block(BaseModel):
    name: str
    elevation: float
    x_offset: float
    y_offset: float

    row_names: List[str]
    seats_per_row: int


class NewStadium(BaseModel):
    name: str
    country: str
    pincode: str
    blocks: List[Block]

