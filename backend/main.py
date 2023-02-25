# pylint: disable=(wrong-import-position, missing-module-docstring)

import os
import dotenv

import fastapi
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
import sqlalchemy as sql
import uvicorn

dotenv.load_dotenv()

from repository.email import Server
from models import database
from models.model import Base

import routes

SENDER_EMAIL_PASSWORD = str(os.getenv("SENDER_EMAIL_PASSWORD"))
SENDER_EMAIL = str(os.getenv("SENDER_EMAIL"))

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
    Server.initialize(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)

    # database.Database().delete_db(Base)
    database.Database().init_db(Base)


app.include_router(routes.tickets_router)
app.include_router(routes.stadium_router)
app.include_router(routes.match_router)

# @app.on_event("shutdown")
# def shutdown_event():
    # Server.server.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
