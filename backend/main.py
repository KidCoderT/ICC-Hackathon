import fastapi
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine
import uvicorn
import schema

app = fastapi.FastAPI()
ticket_routes = fastapi.APIRouter(prefix="/ticket", tags=["ticket_manager"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@ticket_routes.post("/create")
def create_ticket():
    pass


app.include_router(ticket_routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
