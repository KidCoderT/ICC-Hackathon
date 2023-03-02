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
    country_1: str
    country_2: str


class BlockRowInfo(BaseModel):
    name: str
    seats: List[bool]


class BookSeatBlock(BaseModel):
    name: str
    elevation: float
    x_offset: float
    y_offset: float
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
    match_id: int
    stadium_name: str
    block: str
    seat_row: str
    seat_no: int


class NewUser(BaseModel):
    gender: str
    nationality: str
    first_name: str
    last_name: str
    dob: date
    email: str
    phone: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    first_name: str
    last_name: str
    img_path: str

    gender: str
    nationality: str
    dob: date

    email: str
    phone: str
    verified: bool


class LoginUser(BaseModel):
    first_name: str
    last_name: str
    password: str


class UserTicket(BaseModel):
    id: int
    ticket_id: str
    match_id: int
    timestamps: List[datetime]


class Ticket(BaseModel):
    id: int
    match_id: int
    fname: str
    lname: str
    stadium: str
    block: str
    row_name: str
    seat_no: int
    # timestamps: List[str]
    ticket_id: str
