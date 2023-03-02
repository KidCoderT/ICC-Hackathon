import os
import sqlalchemy as sql
import sqlalchemy.orm as orm
from src.patterns import SingletonMeta


__all__ = (
    "Database",
    "db_session",
)

DATABASE_URL = f"mysql+pymysql://{os.getenv('DATABASE_URL')}"


class Database(metaclass=SingletonMeta):
    """This class represents the database connection. It is a singleton class,
    meaning that there will only be one instance of it at any given time. This
    instance will be shared among all the classes that need to access the
    database.
    """

    engine = sql.create_engine(DATABASE_URL, echo=True)
    sessionmaker = orm.sessionmaker(
        autocommit=False, autoflush=False, bind=engine)

    def init_db(self, base):
        base.metadata.create_all(self.engine)

    def delete_db(self, base):
        base.metadata.drop_all(self.engine)


def db_session() -> orm.Session:  # type: ignore
    """Creates a new local database session through which you can access the database and update it.
    This is made using a yield such that finally the session once created will be closed.

    Returns - Session: A new database session.
    """

    db = Database.sessionmaker()

    try:
        yield db
    finally:
        db.close()
