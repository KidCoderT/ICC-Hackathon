import uuid
import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import text
import sqlmodel as sql


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Ticket(sql.SQLModel, table=True):
    id: str = sql.Field(nullable=False, primary_key=True)
    dob: datetime.date

    match_id: Optional[str]
    block_no: str
    seat_no: int
    row_no: str

    gender: Gender = sql.Field(sa_column=sql.Column(sql.Enum(Gender)))
    first_name: str
    last_name: str


# fmt: off

class Match(sql.SQLModel, table=True):
    id: str = sql.Field(
        nullable=False,
        primary_key=True,
        default_factory=lambda: str(uuid.uuid4()),
        index=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
            "unique": True
        }
    )
    start_time: datetime.datetime

# fmt: on
