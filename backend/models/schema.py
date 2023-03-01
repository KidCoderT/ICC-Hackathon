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
    country_1: str
    country_2: str


class UpcommingMatch(BaseModel):
    id: int
    match_format: MatchEnum
    start_time: str
    stadium_name: str
    finished: bool
    booked_seats: int
    total_seats: int


class BlockRowInfo(BaseModel):
    name: str
    seats: List[bool]


class BookSeatBlock(BaseModel):
    name: str
    rows: List[BlockRowInfo]


class BookMatchSeat(BaseModel):
    id: int
    match_format: MatchEnum
    stadium_name: str
    country1: str
    country2: str
    blocks: list[BookSeatBlock]


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
