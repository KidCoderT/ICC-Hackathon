import uuid
import string, secrets
import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base


# todo: there are different match types

__all__ = (
    "Base",
    "Person",
    "Stadium",
    "Block",
    "Seat",
    "Match",
    "Ticket",
)


Base = declarative_base()


def create_ticket_id():
    """Create a new ticket id for a match
    Returns new 6 digit TicketID
    """
    alphabet = string.ascii_letters + string.digits

    while True:
        ticket_id = "".join(secrets.choice(alphabet) for _ in range(6))

        if Ticket.query.filter_by(id=ticket_id, entered=False).first():
            continue

        return ticket_id


class Person(Base):  # type: ignore
    __tablename__ = "person"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    ticket = orm.relationship("Ticket", uselist=False, backref="person")

    gender = sql.Column(sql.Enum("male", "female", "other", name="gender"))
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


class Block(Base):  # type: ignore
    __tablename__ = "blocks"

    name = sql.Column(sql.String(2))
    elevation = sql.Column(sql.Float)
    x_offset = sql.Column(sql.Float)
    y_offset = sql.Column(sql.Float)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    __table_args__ = (
        sql.PrimaryKeyConstraint("name", "stadium_name", name="block_primary_key"),
    )


class Seat(Base):  # type: ignore
    __tablename__ = "seats"

    row_name = sql.Column(sql.String(2), primary_key=True)
    row_no = sql.Column(sql.Integer)
    seat_no = sql.Column(sql.Integer, primary_key=True)

    tickets = orm.relationship("Ticket", backref="seat")

    stadium_name = sql.Column(
        sql.String(255), sql.ForeignKey("stadiums.name"), primary_key=True
    )
    block_name = sql.Column(
        sql.String(2), sql.ForeignKey("blocks.name"), primary_key=True
    )

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
    timing = sql.Column(sql.DateTime)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    stadium = orm.relationship("Stadium", backref="matches")
    tickets = orm.relationship("Ticket", backref="match")

    finished = sql.Column(sql.Boolean(), default=False)


class Ticket(Base):  # type: ignore
    __tablename__ = "tickets"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    ticket_id = sql.Column(sql.String(6), default=create_ticket_id)
    secret_id = sql.Column(sql.String(36), default=str(uuid.uuid4()))
    entered = sql.Column(sql.Boolean(), default=False)
    match_id = sql.Column(sql.Integer, sql.ForeignKey("matches.id"), nullable=False)

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
