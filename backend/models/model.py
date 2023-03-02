import enum
import uuid
import string
import secrets
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, JSON, LargeBinary, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .database import db_session

Base = declarative_base()


class MatchEnum(enum.Enum):
    T20 = "t20"
    ODI = "odi"
    TEST = "test"


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"


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


class IccUser(Base):
    __tablename__ = 'icc_user'

    username = Column(String(50), primary_key=True, unique=True)
    password = Column(String(255))


class Person(Base):
    __tablename__ = 'person'

    first_name = Column(String(50), primary_key=True, nullable=False)
    last_name = Column(String(50), primary_key=True, nullable=False)
    img_path = Column(String(255))
    gender = Column(Enum(GenderEnum, native_enum=True))
    nationality = Column(String(3))
    dob = Column(Date)
    email = Column(String(255))
    phone = Column(String(50))
    verified = Column(TINYINT, server_default=text("'0'"))
    password = Column(String(255))


class Stadium(Base):
    __tablename__ = 'stadiums'

    name = Column(String(255), primary_key=True)
    country = Column(String(3))
    pincode = Column(INTEGER, nullable=False)


class Block(Base):
    __tablename__ = 'blocks'
    __table_args__ = (
        Index('unq_blocks_stadium_name', 'stadium_name', 'name', unique=True),
    )

    name = Column(String(2), primary_key=True, nullable=False)
    elevation = Column(Float)
    x_offset = Column(Float)
    y_offset = Column(Float)
    stadium_name = Column(ForeignKey('stadiums.name'),
                          primary_key=True, nullable=False)

    stadium = relationship('Stadium', backref='blocks')


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    stadium_name = Column(ForeignKey('stadiums.name'), index=True)
    country_1 = Column(String(3))
    country_2 = Column(String(3))
    match_format = Column(Enum(MatchEnum, native_enum=True))
    finished = Column(TINYINT(1), server_default=text("'0'"))

    stadium = relationship('Stadium', backref='matches')

    @property
    def start_time_timestamp(self):
        return int(self.start_time.timestamp())


class Seat(Base):
    __tablename__ = 'seats'
    __table_args__ = (
        Index('seat_index', 'row_name', 'seat_no',
              'block_name', 'stadium_name'),
        Index('uq_seat_row_seat', 'block_name', 'row_name',
              'seat_no', 'stadium_name', unique=True),
        Index('unq_seats_stadium_name', 'stadium_name',
              'block_name', 'row_name', 'seat_no', unique=True)
    )

    row_name = Column(String(2), primary_key=True, nullable=False)
    row_no = Column(Integer)
    seat_no = Column(Integer, primary_key=True, nullable=False)
    stadium_name = Column(ForeignKey('stadiums.name'),
                          primary_key=True, nullable=False)
    block_name = Column(ForeignKey('blocks.name'),
                        primary_key=True, nullable=False, index=True)

    block = relationship('Block', backref='seats')
    stadium = relationship('Stadium', backref='seats')


class TempTicket(Base):
    __tablename__ = 'temp_ticket'
    __table_args__ = (
        ForeignKeyConstraint(['fname', 'lname'], [
                             'person.first_name', 'person.last_name']),
        ForeignKeyConstraint(['stadium', 'block'], [
                             'blocks.stadium_name', 'blocks.name']),
        Index('block', 'stadium', 'block'),
        Index('person', 'fname', 'lname')
    )

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, nullable=False)
    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)
    stadium = Column(ForeignKey('stadiums.name'), nullable=False)
    block = Column(String(2), nullable=False)
    row_name = Column(String(2), nullable=False)
    seat_no = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False,
                       server_default=text("CURRENT_TIMESTAMP"))

    person = relationship('Person')
    block1 = relationship('Block')
    stadium1 = relationship('Stadium')


class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = (
        ForeignKeyConstraint(['fname', 'lname'], [
                             'person.first_name', 'person.last_name']),
        ForeignKeyConstraint(['stadium', 'block', 'row_name', 'seat_no'], [
                             'seats.stadium_name', 'seats.block_name', 'seats.row_name', 'seats.seat_no']),
        ForeignKeyConstraint(['stadium', 'block'], [
                             'blocks.stadium_name', 'blocks.name']),
        Index('seat', 'stadium', 'block', 'row_name', 'seat_no'),
        Index('block_1', 'stadium', 'block'),
        Index('secret', 'match_id', 'ticket_id'),
        Index('person_1', 'fname', 'lname')
    )

    id = Column(Integer, primary_key=True)
    match_id = Column(ForeignKey('matches.id'), nullable=False)
    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)
    stadium = Column(ForeignKey('stadiums.name'), nullable=False)
    block = Column(String(2), nullable=False)
    row_name = Column(String(2), nullable=False)
    seat_no = Column(Integer, nullable=False)
    timestamps = Column(JSON, nullable=False, default=[""])
    ticket_id = Column(String(6), default=create_ticket_id)
    secret_id = Column(String(36), default=lambda: str(uuid.uuid4()))
    qrcode = Column(LargeBinary, nullable=True, default=None)

    person = relationship('Person', backref='tickets')
    match = relationship('Match', backref='tickets')
    seat = relationship('Seat', backref='tickets')
    block1 = relationship('Block', backref='tickets')
    stadium1 = relationship('Stadium', backref='tickets')
