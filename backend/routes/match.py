from enum import Enum
from typing import Any, Dict, List

import fastapi
from fastapi import Depends
from models.database import db_session, orm
from models import schema, model

router = fastapi.APIRouter(prefix="/match", tags=["matches_manager"])

# todo: order by finished or not


@router.post("/create")
def new_match(new_match: schema.NewMatch, db: orm.Session = Depends(db_session)):
    match = model.Match(
        start_time=new_match.start_time,
        stadium_name=new_match.stadium_name,
    )

    # todo: create a schedular to end_match

    db.add(match)
    db.commit()
    db.refresh(match)

    return fastapi.responses.JSONResponse(
        content={
            "status": "CREATED",
            "msg": "New Match Created",
            "model": schema.Match(**match.__dict__),
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.get("/all", response_model=List[schema.Match])
def all_matches(db: orm.Session = Depends(db_session)):
    return list(map(lambda x: x.__dict__, db.query(model.Match).all()))


@router.get("/get/{id}")
def get_match(
    id: int,
    db: orm.Session = Depends(db_session),
):
    match = db.query(model.Match).get(id)

    if match:
        return match.__dict__

    raise fastapi.exceptions.HTTPException(
        detail={"STATUS": "NOT FOUND", "msg": "Matcg Not Found"},
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
    )


class MatchFetchParam(Enum):
    ALL = "all"
    FINISHED_ONLY = "finished"
    UNFINISHED_ONLY = "unfinished"
    CURRENTLY = "currently"


@router.get("/stadium/{name}")
def get_stadium_matches(
    name: str,
    fetch_param: MatchFetchParam,
    db: orm.Session = Depends(db_session),
):
    query_params: Dict[str, Any] = {"stadium_name": name}

    # if finished_matches:
    #     query_params["finished"] = True
    # todo: add matching for fetch_param

    matches = db.query(model.Match).filter_by(**query_params).all()
    return list(map(lambda x: x.__dict__, matches))
