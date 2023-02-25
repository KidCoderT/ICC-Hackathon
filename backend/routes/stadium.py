from typing import List
import fastapi
from fastapi import Depends
from models.database import db_session, orm
from models import schema, model

router = fastapi.APIRouter(prefix="/stadium", tags=["stadiums_manager"])


@router.post("/create")
def new_stadium(new_stadium: schema.NewStadium, db: orm.Session = Depends(db_session)):
    stadium = model.Stadium(
        name=new_stadium.name,
        country=new_stadium.country,
        pincode=new_stadium.pincode,
    )

    db.add(stadium)
    db.commit()

    for block in new_stadium.blocks:
        new_block = model.Block(
            name=block.name,
            elevation=block.elevation,
            x_offset=block.x_offset,
            y_offset=block.y_offset,
            stadium_name=stadium.name,
        )

        db.add(new_block)
        db.commit()

        for i, row_name in enumerate(block.row_names):
            for j in range(block.seats_per_row):
                new_seat = model.Seat(
                    row_name=row_name,
                    row_no=i,
                    seat_no=j,
                    stadium_name=stadium.name,
                    block_name=new_block.name,
                )

                db.add(new_seat)

        db.commit()

    db.refresh(stadium)

    return fastapi.responses.JSONResponse(
        content={
            "status": "CREATED",
            "msg": "New Stadium Added to DB",
            "model": schema.Stadium(**stadium.__dict__),
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.get("/all", response_model=List[schema.Stadium])
def all_stadiums(db: orm.Session = Depends(db_session)):
    return list(map(lambda x: x.__dict__, db.query(model.Stadium).all()))


@router.get("/get/stadium")
def get_stadium(
    request: schema.FetchStadium,
    db: orm.Session = Depends(db_session),
):
    stadium = (
        db.query(model.Stadium)
        .filter_by(stadium_name=request.stadium_name)
        .one_or_none()
    )

    if stadium:
        return stadium.__dict__

    raise fastapi.exceptions.HTTPException(
        detail={"STATUS": "NOT FOUND", "msg": "Block Not Found"},
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.get("/get/block")
def get_block(
    request: schema.FetchBlock,
    db: orm.Session = Depends(db_session),
):
    block = (
        db.query(model.Block)
        .filter_by(
            name=request.block_name,
            stadium_name=request.stadium_name,
        )
        .one_or_none()
    )

    if block:
        return block.__dict__

    raise fastapi.exceptions.HTTPException(
        detail={"STATUS": "NOT FOUND", "msg": "Block Not Found"},
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.get("/get/seat")
def get_seat(
    request: schema.FetchSeat,
    db: orm.Session = Depends(db_session),
):
    seat = (
        db.query(model.Seat)
        .filter_by(
            row_name=request.row_name,
            seat_no=request.seat_no,
            block_name=request.block_name,
            stadium_name=request.stadium_name,
        )
        .one_or_none()
    )

    if seat:
        return seat.__dict__

    raise fastapi.exceptions.HTTPException(
        detail={"STATUS": "NOT FOUND", "msg": "Seat Not Found"},
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )
