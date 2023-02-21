import string
import secrets
import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base


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
    alphabet = string.ascii_letters + string.digits

    while True:
        ticket_id = "".join(secrets.choice(alphabet) for _ in range(6))

        if Ticket.query.filter_by(id=ticket_id).first():
            continue

        return ticket_id


class Person(Base):
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


class Stadium(Base):
    __tablename__ = "stadiums"

    name = sql.Column(sql.String(255), primary_key=True)
    country = sql.Column(sql.String(255))
    pincode = sql.Column(sql.String(10))


class Block(Base):
    __tablename__ = "blocks"

    name = sql.Column(sql.String(2))
    elevation = sql.Column(sql.Float)
    x_offset = sql.Column(sql.Float)
    y_offset = sql.Column(sql.Float)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    __table_args__ = (sql.PrimaryKeyConstraint(
        "name", "stadium_name", name="block_primary_key"),)


class Seat(Base):
    __tablename__ = "seats"

    row_name = sql.Column(sql.String(2))
    column = sql.Column(sql.Integer)
    row = sql.Column(sql.Integer)

    tickets = orm.relationship("Ticket", backref="seat")

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    block_name = sql.Column(sql.String(2), sql.ForeignKey("blocks.name"))

    __table_args__ = (
        sql.PrimaryKeyConstraint(
            "row_name", "block_name", "stadium_name", name="seat_primary_key"),
    )


class Match(Base):
    __tablename__ = "matches"
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    timing = sql.Column(sql.DateTime)

    stadium_name = sql.Column(sql.String(255), sql.ForeignKey("stadiums.name"))
    stadium = orm.relationship("Stadium", backref="matches")
    tickets = orm.relationship("Ticket", backref="match")


class Ticket(Base):
    __tablename__ = "tickets"
    id = sql.Column(sql.String(6), primary_key=True, default=create_ticket_id)

    person_id = sql.Column(
        sql.Integer, sql.ForeignKey("person.id"), nullable=False)
    match_id = sql.Column(sql.Integer, sql.ForeignKey(
        "matches.id"), nullable=False)
    seat_id = sql.Column(sql.String(255), sql.ForeignKey("seats.row_name"))

    # todo: __str__
