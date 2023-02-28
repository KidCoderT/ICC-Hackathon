import enum
import uuid
import string
import secrets
from datetime import datetime

import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGBLOB

from .database import db_session


__all__ = (
    "Base",
    "Person",
    "Stadium",
    "Block",
    "Seat",
    "Match",
    "Ticket",
    "IccUser",
)


Base = declarative_base()


def create_ticket_id():
    """Create a new ticket id for a match
    Returns new 6 digit TicketID
    """
    alphabet = string.ascii_letters + string.digits
    databse = db_session()
    session = next(databse)

    while True:
        ticket_id = "".join(secrets.choice(alphabet) for _ in range(6))

        if session.query(Ticket).filter_by(id=ticket_id).first():
            continue

        try:
            next(databse)
        except StopIteration:
            pass

        return ticket_id


class MatchEnum(enum.Enum):
    T20 = "t20"
    ODI = "odi"
    TEST = "test"


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Person(Base):  # type: ignore
    __tablename__ = "person"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    ticket = orm.relationship("Ticket", uselist=False, backref="person")
    image = sql.Column(sql.LargeBinary(length=(2**32) - 1))

    gender = sql.Column(sql.Enum(GenderEnum, native_enum=True))
    nationality = sql.Column(sql.String(3))
    first_name = sql.Column(sql.String(50))
    last_name = sql.Column(sql.String(50))
    dob = sql.Column(sql.Date)

    email = sql.Column(sql.String(255))
    phone = sql.Column(sql.String(20))

    ticket = orm.relationship("Ticket", back_populates="person", uselist=False)


class Stadium(Base):  # type: ignore
    __tablename__ = "stadiums"

    name = sql.Column(sql.String(255), primary_key=True)
    country = sql.Column(sql.String(255))
    pincode = sql.Column(sql.String(10))

    blocks = orm.relationship("Block", backref="stadium")


class Block(Base):  # type: ignore
    __tablename__ = "blocks"

    name = sql.Column(sql.String(2))
    elevation = sql.Column(sql.Float)
    x_offset = sql.Column(sql.Float)
    y_offset = sql.Column(sql.Float)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    seats = orm.relationship("Seat", backref="block")

    __table_args__ = (
        sql.PrimaryKeyConstraint(
            "name", "stadium_name", name="block_primary_key"),
    )


class Seat(Base):  # type: ignore
    __tablename__ = "seats"

    row_name = sql.Column(sql.String(2), primary_key=True)
    row_no = sql.Column(sql.Integer)
    seat_no = sql.Column(sql.Integer, primary_key=True)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey(
        "stadiums.name"), primary_key=True)
    block_name = sql.Column(sql.String(2), sql.ForeignKey(
        "blocks.name"), primary_key=True)

    __table_args__ = (
        sql.UniqueConstraint(
            "row_name", "seat_no", "block_name", "stadium_name", name="uq_seat_row_seat"
        ),
        sql.Index(
            "idx_seats_row_seat_block_stadium",
            "row_name",
            "seat_no",
            "block_name",
            "stadium_name",
        ),
    )


class Match(Base):  # type: ignore
    __tablename__ = "matches"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    start_time = sql.Column(sql.DateTime)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    stadium = orm.relationship("Stadium", backref="matches")
    tickets = orm.relationship("Ticket", backref="match")

    country_1 = sql.Column(sql.String(3))
    country_2 = sql.Column(sql.String(3))

    match_format = sql.Column(sql.Enum(MatchEnum, native_enum=True))

    finished = sql.Column(sql.Boolean(), default=False)


class Ticket(Base):  # type: ignore
    __tablename__ = "tickets"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    ticket_id = sql.Column(sql.String(6), default=create_ticket_id)
    secret_id = sql.Column(sql.String(
        36), default=lambda: str(uuid.uuid4()), unique=True)
    match_id = sql.Column(sql.Integer, sql.ForeignKey(
        "matches.id"), nullable=False)

    qrcode = sql.Column(sql.LargeBinary, nullable=True)

    timestamps = sql.Column(sql.JSON)

    person_id = sql.Column(
        sql.Integer,
        sql.ForeignKey("person.id"),
        unique=True,
        nullable=False,
    )

    stadium_name = sql.Column(
        sql.String(255),
        sql.ForeignKey("stadiums.name"),
        nullable=False,
    )

    block_name = sql.Column(
        sql.String(255),
        sql.ForeignKey("blocks.name"),
        nullable=False,
    )

    seat_row = sql.Column(
        sql.String(255),
        sql.ForeignKey("seats.row_name"),
        nullable=False,
    )

    seat_no = sql.Column(
        sql.Integer,
        nullable=False,
    )

    person = orm.relationship("Person", back_populates="ticket")

    __table_args__ = (
        sql.ForeignKeyConstraint(
            ["seat_row", "seat_no", "block_name", "stadium_name"],
            [
                "seats.row_name",
                "seats.seat_no",
                "seats.block_name",
                "seats.stadium_name",
            ],
            name="fk_ticket_seat",
        ),
        sql.ForeignKeyConstraint(
            ["block_name", "stadium_name"],
            ["blocks.name", "blocks.stadium_name"],
            name="fk_ticket_block",
        ),
    )


class TempTicket(Base):
    __tablename__ = "temp_ticket"

    id = sql.Column(sql.String(
        36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    person = sql.Column(sql.Integer, sql.ForeignKey("person.id"))
    match_id = sql.Column(sql.Integer, sql.ForeignKey("matches.id"))

    stadium_name = sql.Column(
        sql.String(255),
        sql.ForeignKey("stadiums.name"),
        nullable=False
    )
    block_name = sql.Column(
        sql.String(255),
        sql.ForeignKey("blocks.name"),
        nullable=False
    )
    seat_row = sql.Column(
        sql.String(255),
        sql.ForeignKey("seats.row_name"),
        nullable=False
    )
    seat_no = sql.Column(
        sql.Integer,
        nullable=False
    )

    timestamp = sql.Column(sql.DateTime, default=datetime.utcnow)


class IccUser(Base):  # type: ignore
    __tablename__ = "icc_user"
    username = sql.Column(sql.String(50), nullable=False,
                          primary_key=True, unique=True)
    password = sql.Column(sql.String(255))
