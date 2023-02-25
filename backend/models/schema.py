from typing import List
from datetime import datetime
from pydantic import BaseModel

from .model import MatchEnum


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


class Stadium(BaseModel):
    name: str
    country: str
    pincode: str


class FetchStadium(BaseModel):
    stadium_name: str


class FetchBlock(FetchStadium):
    block_name: str


class FetchSeat(FetchBlock):
    row_name: str
    seat_no: int


class NewMatch(BaseModel):
    start_time: datetime
    stadium_name: str
    match_format: MatchEnum


class Match(BaseModel):
    id: int
    match_format: MatchEnum
    start_time: datetime
    stadium_name: str
    finished: bool

