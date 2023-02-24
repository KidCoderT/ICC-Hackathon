from typing import List
import fastapi
from fastapi import Depends
from models.database import db_session, orm
from models import schema, model

router = fastapi.APIRouter(prefix="/match", tags=["matches_manager"])


@router.post("/create")
def new_match(new_match: schema.NewMatch, db: orm.Session = Depends(db_session)):
    match = model.Match(
        start_time=new_match.start_time,
        stadium_name=new_match.stadium_name,
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return fastapi.responses.JSONResponse(
        content={
            "status": "CREATED",
            "msg": "New Match Created",
            "model": match.__dict__,
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.get("/all", response_model=List[schema.Match])
def all_matches(db: orm.Session = Depends(db_session)):
    return list(map(lambda x: x.__dict__, db.query(model.Match).all()))
