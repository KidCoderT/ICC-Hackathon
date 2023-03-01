from typing import List, Optional
from datetime import datetime, date
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


class NewMatch(BaseModel):
    start_time: datetime
    stadium_name: str
    match_format: MatchEnum
    country_1: str
    country_2: str


class Match(BaseModel):
    id: int
    match_format: MatchEnum
    start_time: datetime
    stadium_name: str
    finished: bool


class FetchStadiumMatches(BaseModel):
    stadium_name: str
    fetch_param: Optional[MatchEnum] = None
    all: bool = True


class NewTicket(BaseModel):
    gender: str
    nationality: str
    first_name: str
    last_name: str
    dob: date
    email: str
    phone: str

    match_id: int
    stadium_name: str
    block: str
    seat_row: str
    seat_no: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
