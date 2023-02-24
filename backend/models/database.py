import os
import sqlalchemy as sql
import sqlalchemy.orm as orm


__all__ = (
    "Database",
    "db_session",
)

DATABASE_URL = f"mysql+pymysql://{os.getenv('DATABASE_URL')}"


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """This class represents the database connection. It is a singleton class,
    meaning that there will only be one instance of it at any given time. This
    instance will be shared among all the classes that need to access the
    database.
    """

    engine = sql.create_engine(DATABASE_URL, echo=True)
    sessionmaker = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
