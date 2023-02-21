import os
import dotenv
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as orm
import sqlalchemy as sql
import uvicorn
import schema

dotenv.load_dotenv()

app = fastapi.FastAPI()
ticket_routes = fastapi.APIRouter(prefix="/ticket", tags=["ticket_manager"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = f"mysql+pymysql://{os.getenv('DB_LOCATION')}"

engine = sql.create_engine(DATABASE, echo=True)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.on_event("startup")
def on_startup():
    schema.Base.metadata.create_all(engine)


@ticket_routes.post("/create")
def create_ticket():
    pass


app.include_router(ticket_routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
