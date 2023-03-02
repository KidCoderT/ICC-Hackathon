from typing import Any, Dict, List, Optional
from datetime import datetime

import fastapi
from fastapi import Depends
from models.database import db_session, orm
from models import schema, model

from .auth import current_user

router = fastapi.APIRouter(prefix="/match", tags=["matches_manager"])


@router.post("/create")
def new_match(new_match: schema.NewMatch, icc=Depends(current_user), db: orm.Session = Depends(db_session)):

    if db.query(model.Stadium).filter_by(name=new_match.stadium_name).one_or_none() is None:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Stadium Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    match = model.Match(
        start_time=new_match.start_time,
        stadium_name=new_match.stadium_name,
        match_format=new_match.match_format,
        country_1=new_match.country_1,
        country_2=new_match.country_2
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return fastapi.responses.JSONResponse(
        content={
            "status": "CREATED",
            "msg": "New Match Created",
            # "model": schema.Match(**match.__dict__),
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.get("/all", response_model=List[schema.UpcommingMatch])
def all_matches(db: orm.Session = Depends(db_session)):
    all_matches: List[model.Match] = db.query(model.Match).all()
    result = []

    for match in all_matches:
        all_stadium_seats = db.query(model.Seat).filter_by(
            stadium_name=match.stadium_name).all()
        booked_seats = db.query(model.Ticket).filter_by(match_id=match.id).all(
        ) + db.query(model.TempTicket).filter_by(match_id=match.id).all()
        result.append(
            schema.UpcommingMatch(
                id=match.id,
                match_format=match.match_format,
                start_time=match.start_time_timestamp,
                stadium_name=match.stadium_name,
                booked_seats=len(booked_seats),
                total_seats=len(all_stadium_seats),
                finished=match.finished,
                country_1=match.country_1,
                country_2=match.country_2
            )
        )

    return result


@router.get("/get/{match_id}")
def get_match(
    match_id: int,
    db: orm.Session = Depends(db_session),
) -> schema.BookMatchSeat:
    match: Optional[model.Match] = db.query(model.Match).get(match_id)

    if not match:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Match Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    booked_seats = [(ticket.row_name, ticket.seat_no)
                    for ticket in match.tickets]

    blocks = []

    for block in match.stadium.blocks:
        block: model.Block = block
        block_data = schema.BookSeatBlock(
            name=block.name, elevation=block.elevation, x_offset=block.x_offset, y_offset=block.y_offset, rows=[])

        row_names = {}

        for seat in block.seats:
            seat: model.Seat = seat

            try:
                row_names[seat.row_name].append(seat.seat_no)
            except:
                row_names[seat.row_name] = [seat.seat_no]

        raw_rows = [[
            name, sorted(row)] for name, row in row_names.items()]

        for idx in range(len(raw_rows)):
            raw_rows[idx][1] = [(raw_rows[idx][0], value)
                                in booked_seats for value in raw_rows[idx][1]]

        block_data.rows = [schema.BlockRowInfo(
            name=data[0], seats=data[1]) for data in raw_rows]

        blocks.append(block_data)

    return schema.BookMatchSeat(id=match.id, match_format=match.match_format, stadium_name=match.stadium_name, country1=match.country_1, country2=match.country_2, blocks=blocks)


@router.get("/stadium/{stadium_name}")
def get_stadium_matches(
    stadium_name: str,
    db: orm.Session = Depends(db_session),
):
    all_matches: List[model.Match] = db.query(model.Match).filter_by(
        **{"stadium_name": stadium_name}).all()
    result = []

    for match in all_matches:
        all_stadium_seats = db.query(model.Seat).filter_by(
            stadium_name=match.stadium_name).all()
        booked_seats = db.query(model.Ticket).filter_by(match_id=match.id).all(
        ) + db.query(model.TempTicket).filter_by(match_id=match.id).all()
        result.append(
            schema.UpcommingMatch(
                id=match.id,
                match_format=match.match_format.value,
                start_time=match.start_time_timestamp,
                stadium_name=match.stadium_name,
                booked_seats=len(booked_seats),
                total_seats=len(all_stadium_seats),
                finished=match.finished
            )
        )

    return result


@router.post("/end/{id}")
def end_match(
    id: int, icc=Depends(current_user),
    db: orm.Session = Depends(db_session),
):
    # fixme soon
    matches = db.query(model.Match).get(id)

    if not matches:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Matcg Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    matches.ended = True
    db.commit()

    return fastapi.responses.JSONResponse(
        content={
            "status": "OK",
            "msg": "Ended Match",
        },
        status_code=fastapi.status.HTTP_200_OK,
    )
