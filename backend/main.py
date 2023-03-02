# pylint: disable=(wrong-import-position, missing-module-docstring)

import os
import dotenv

import fastapi
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
import sqlalchemy as sql
import uvicorn

dotenv.load_dotenv()

from models import database
from models.model import Base
import routes


app = fastapi.FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # database.Database().delete_db(Base)
    database.Database().init_db(Base)


app.include_router(routes.tickets_router)
app.include_router(routes.stadium_router)
app.include_router(routes.person_router)
app.include_router(routes.match_router)
app.include_router(routes.auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
