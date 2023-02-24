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
        content={"status": "CREATED", "msg": "New Stadium Added to DB"},
        status_code=fastapi.status.HTTP_201_CREATED,
    )


# todo: access block, access seat
