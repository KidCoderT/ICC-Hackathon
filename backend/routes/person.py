import io
import imghdr
import json
from typing import Optional
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from smtplib import SMTPRecipientsRefused, SMTP_SSL
from jose import jwt, JWTError, ExpiredSignatureError

import qrcode
import fastapi
from fastapi import Depends, File, UploadFile
from sqlalchemy import LargeBinary

from models.database import db_session, orm
from models import schema, model

from src import tokens, check
from src.email import smtp_server, SENDER_EMAIL
from .auth import current_user

router = fastapi.APIRouter(prefix="/person", tags=["people_manager"])


@router.post("/create/{json_info}")
def create_person(
    json_info: str,
    image_file: UploadFile,
    server: SMTP_SSL = Depends(smtp_server),
    db: orm.Session = Depends(db_session)
):
    image_bytes = image_file.file.read()
    is_valid_img = imghdr.what(image_file.filename, image_bytes)

    if not is_valid_img:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "INVALID FILE", "msg": "image type is invalid"},
            status_code=fastapi.status.HTTP_406_NOT_ACCEPTABLE,
        )

    new_user_info = schema.NewUser(**json.loads(json_info))

    users = db.query(model.Person).filter_by(
        first_name=new_user_info.first_name, last_name=new_user_info.last_name).all()

    if len(users) > 0:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_302_FOUND, detail={
                                    "status": "USER FOUND", "msg": "user already exists in db"})

    file_path = f"photos/{new_user_info.first_name}-{new_user_info.last_name}.{image_file.filename.split('.')[-1]}"
    with open(file_path, "wb") as buffer:
        buffer.write(image_bytes)

    person = model.Person(
        gender=new_user_info.gender,
        nationality=new_user_info.nationality,
        first_name=new_user_info.first_name,
        last_name=new_user_info.last_name,
        dob=new_user_info.dob,
        email=new_user_info.email,
        phone=new_user_info.phone,
        password=check.hash_password(new_user_info.password),
        img_path=file_path
    )

    db.add(person)
    db.commit()

    token = tokens.create_access_token(
        {"fname": person.first_name, "lname": person.last_name, "password": person.password})

    subject = "verify account"
    message = f'Hi please verify you account<br>\
        <form action="https://localhost:8080/person/verify" method="post">\
            <input type="hidden" name="token" value="{token}">\
            <input type="submit" value="Click Here">\
        </form>'

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = person.email
    msg["Subject"] = subject

    text = MIMEText(message, "html")
    msg.attach(text)

    try:
        server.sendmail(SENDER_EMAIL, person.email, msg.as_string())
    except SMTPRecipientsRefused as exc:
        db.delete(person)
        db.commit()

        return fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "FAILED",
                "message": (
                    f"because of {str(exc)} We were not able to send an "
                    "email to u and hence creation of your user failed! "
                    "please try again after some time!!"
                ),
            },
        )

    return fastapi.responses.JSONResponse(
        content={
            "status": "VERIFICATION SENT",
            "msg": "Please check your email to verify its you!"
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.post("/verify")
def verify_person(token: str = fastapi.Form(), db: orm.Session = Depends(db_session)):
    try:
        data = tokens.decrypt_token(token)
    except (JWTError, ExpiredSignatureError) as exc:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "TOKEN EXPIRTED",
                "message": "Token has expired / has some error"
            },
        ) from exc

    person: Optional[model.Person] = db.query(model.Person).filter_by(
        first_name=data.get("fname"), last_name=data.get("lname"), password=data.get("password")).one_or_none()

    if person is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "DATA INVALID",
                "message": "Person is not There"
            },
        )

    person.verified = True

    db.commit()

    return fastapi.responses.JSONResponse(
        content={
            "status": "DONE",
            "msg": "User VERIFIED"
        },
        status_code=fastapi.status.HTTP_200_OK,
    )


@router.post("/verify/resend")
def resend_verification(first_name: str, last_name: str, password: str, server: SMTP_SSL = Depends(smtp_server), db: orm.Session = Depends(db_session)):
    person: Optional[model.Person] = db.query(model.Person).filter_by(
        first_name=first_name, last_name=last_name).one_or_none()

    if person is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "DATA INVALID",
                "message": "Person is not There"
            },
        )

    if not check.verify_password(password, person.password):
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "INVALID DATA",
                "message": "Password is Incorrect"
            },
        )

    if person.verified:
        return fastapi.responses.JSONResponse(
            content={
                "status": "ALREADY VERIFIED",
                "msg": "You are already Verified!"
            },
            status_code=fastapi.status.HTTP_201_CREATED,
        )

    token = tokens.create_access_token(
        {"fname": first_name, "lname": last_name, "password": person.password})

    subject = "verify account"
    message = f'Hi please verify you account<br>\
        <form action="https://localhost:8080/person/verify" method="post">\
            <input type="hidden" name="token" value="{token}">\
            <input type="submit" value="Click Here">\
        </form>'

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = person.email
    msg["Subject"] = subject

    text = MIMEText(message, "html")
    msg.attach(text)

    try:
        server.sendmail(SENDER_EMAIL, person.email, msg.as_string())
    except SMTPRecipientsRefused as exc:
        db.delete(person)
        db.commit()

        return fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "FAILED",
                "message": (
                    f"because of {str(exc)} We were not able to send an "
                    "email to u and hence creation of your user failed! "
                    "please try again after some time!!"
                ),
            },
        )

    return fastapi.responses.JSONResponse(
        content={
            "status": "VERIFICATION RESENT",
            "msg": "Please check your email to verify its you!"
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


@router.get("/me")
def person(first_name: str, last_name: str, password: str, db: orm.Session = Depends(db_session)):
    person: Optional[model.Person] = db.query(model.Person).filter_by(
        first_name=first_name, last_name=last_name).one_or_none()

    if person is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "DATA INVALID",
                "message": "Person is not There"
            },
        )

    if not check.verify_password(password, person.password):
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "INVALID DATA",
                "message": "Password is Incorrect"
            },
        )

    return schema.User(
        first_name=person.first_name,
        last_name=person.last_name,
        img_path=person.img_path,
        gender=person.gender.value,
        nationality=person.nationality,
        dob=str(person.dob),
        email=person.email,
        phone=person.phone,
        verified=person.verified
    )


@router.get("/mine")
def person_tickets(first_name: str, last_name: str, password: str, db: orm.Session = Depends(db_session)):
    person: Optional[model.Person] = db.query(model.Person).filter_by(
        first_name=first_name, last_name=last_name).one_or_none()

    if person is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "DATA INVALID",
                "message": "Person is not There"
            },
        )

    if not check.verify_password(password, person.password):
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "INVALID DATA",
                "message": "Password is Incorrect"
            },
        )

    tickets = db.query(model.Ticket).filter_by(
        fname=person.first_name, lname=person.last_name).all()

    return [schema.Ticket(**ticket.__dict__) for ticket in tickets]
