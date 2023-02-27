
from typing import Optional
import fastapi
import fastapi.security
from models.database import db_session, orm
from models import schema, model
import src.tokens
import src.check

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/auth/login")


def current_user(
    token: str = fastapi.Depends(oauth2_scheme),
):
    """Returns the username of the current user based on the given token.
    If the token is invalid, raises a 401 Unauthorized exception.
    Parameters - token (str): The access token to be verified.
    Returns - models.schema.TokenData: The data stored in the token.
    Raises - fastapi.HTTPException: If the token is invalid.
    """

    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return src.tokens.verify_token(token, credentials_exception)


router = fastapi.APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    request: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(),
    database: orm.Session = fastapi.Depends(model.db_session),
):
    """Attempts to log in a user with the provided username and password.
    Parameters:
        - request: fastapi.security.OAuth2PasswordRequestForm: The username and password to authenticate with.
        - database: Session: A database session to use for querying the user information.
    Returns: - dict: A dictionary containing the access token and token type.
    Raises: - fastapi.HTTPException: If the provided username or password is invalid.
    """

    user: Optional[model.IccUser] = database.query(model.IccUser).filter_by(
        username=request.username).one_or_none()

    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )

    if not src.check.verify_password(request.password, user.password):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password, Try Again!",
        )

    access_token = src.tokens.create_access_token(
        data={"sub": user.username}, expires_info={"minutes": 30})
    return {"status": "OK", "access_token": access_token, "token_type": "bearer"}
