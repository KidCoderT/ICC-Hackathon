from typing import Any, Dict, List, Optional

import fastapi
from fastapi import Depends
from models.database import db_session, orm
from models import schema, model

router = fastapi.APIRouter(prefix="/match", tags=["matches_manager"])


@router.post("/create")
def new_match(new_match: schema.NewMatch, db: orm.Session = Depends(db_session)):

    if db.query(model.Stadium).filter_by(name=new_match.stadium_name).one_or_none() is None:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Stadium Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    match = model.Match(
        start_time=new_match.start_time,
        stadium_name=new_match.stadium_name,
        match_format=new_match.match_format,
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


@router.get("/all", response_model=List[schema.Match])
def all_matches(db: orm.Session = Depends(db_session)):
    return list(map(lambda x: x.__dict__, db.query(model.Match).all()))


@router.get("/get/{match_id}")
def get_match(
    match_id: int,
    db: orm.Session = Depends(db_session),
):
    match = db.query(model.Match).get(match_id)

    if match:
        return match.__dict__

    raise fastapi.exceptions.HTTPException(
        detail={"STATUS": "NOT FOUND", "msg": "Match Not Found"},
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


@router.get("/stadium/{stadium_name}")
def get_stadium_matches(
    stadium_name: str,
    fetch_param: Optional[int] = None,
    show_all: bool = True,
    db: orm.Session = Depends(db_session),
):
    query_params: Dict[str, Any] = {"stadium_name": stadium_name}

    if not show_all:
        query_params["finished"] = False

    if fetch_param is not None:
        query_params["match_format"] = fetch_param

    matches = db.query(model.Match).filter_by(**query_params).all()
    return list(map(lambda x: x.__dict__, matches))


@router.post("/end/{id}")
def end_match(
    id: int,
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
