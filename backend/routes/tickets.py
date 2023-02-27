from typing import Optional
from datetime import datetime, timedelta
from smtplib import SMTPRecipientsRefused, SMTP_SSL
from jose import jwt, JWTError, ExpiredSignatureError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import qrcode
import fastapi
from fastapi import Depends
import rsa

from models.database import db_session, orm
from models import schema, model

from src import tokens
from src.email import smtp_server, SENDER_EMAIL
from .auth import current_user

router = fastapi.APIRouter(prefix="/ticket", tags=["tickets_manager"])


@router.post("/create")
def create_ticket(new_ticket_info: schema.NewTicket, server: SMTP_SSL = Depends(smtp_server), db: orm.Session = Depends(db_session)):

    stadium: Optional[model.Stadium] = db.query(model.Stadium).filter_by(
        name=new_ticket_info.stadium_name).one_or_none()

    if stadium is None:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Stadium Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    block_names = [block.name for block in stadium.blocks]

    if new_ticket_info.block not in block_names:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Block Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    block = stadium.blocks[block_names.index(new_ticket_info.block)]
    seat = list(filter(lambda seat: seat.row_name ==
                new_ticket_info.seat_row and seat.seat_no == new_ticket_info.seat_no, block.seats))

    if len(seat) != 1:
        raise fastapi.exceptions.HTTPException(
            detail={"STATUS": "NOT FOUND", "msg": "Seat Not Found"},
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Set the conditions for the query
    conditions = {
        "match_id": new_ticket_info.match_id,
        "stadium_name": new_ticket_info.stadium_name,
        "block_name": new_ticket_info.block,
        "seat_row": new_ticket_info.seat_row,
        "seat_no": new_ticket_info.seat_no,
    }

    query = db.query(model.Ticket).filter(
        *[(getattr(model.Ticket, key) == conditions[key]) for key in conditions]
    )

    if query.one_or_none() is not None:
        return fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "FAILED",
                "message": "too slow someone is already booked that seat"
            },
        )

    # Calculate the timestamp 30 minutes before the current time
    cutoff_time = datetime.utcnow() - timedelta(minutes=30)

    query = db.query(model.TempTicket).filter(
        model.TempTicket.timestamp >= cutoff_time,
        *[(getattr(model.TempTicket, key) == conditions[key]) for key in conditions]
    )

    if query.one_or_none() is not None:
        return fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "FAILED",
                "message": "too slow someone is on the verge of booking that seat"
            },
        )

    # add response if input wrong

    person = model.Person(
        gender=new_ticket_info.gender,
        nationality=new_ticket_info.nationality,
        first_name=new_ticket_info.first_name,
        last_name=new_ticket_info.last_name,
        dob=new_ticket_info.dob,
        email=new_ticket_info.email,
        phone=new_ticket_info.phone,
    )

    db.add(person)
    db.commit()
    db.refresh(person)

    temp_ticket = model.TempTicket(
        person=person.id,
        match_id=new_ticket_info.match_id,
        stadium_name=new_ticket_info.stadium_name,
        block_name=new_ticket_info.block,
        seat_row=new_ticket_info.seat_row,
        seat_no=new_ticket_info.seat_no
    )

    db.add(temp_ticket)
    db.commit()
    db.refresh(temp_ticket)

    token = tokens.create_access_token({"temp_ticket": temp_ticket.id})

    subject = "verify token"
    message = f'Hi please verify you account<br>\
        <form action="https://kvkpop-effective-xylophone-5666r65j655cvwgx-8080.preview.app.github.dev/ticket/generate" method="post">\
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
        db.delete(temp_ticket)
        db.commit()

        return fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "FAILED",
                "message": (
                    f"because of {str(exc)} We were not able to send an "
                    "email to u and hence creation of your ticket failed! "
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


@router.post("/generate")
def generate_ticket(token: str = fastapi.Form(), server: SMTP_SSL = Depends(smtp_server), db: orm.Session = Depends(db_session)):
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

    temp_ticket: Optional[model.TempTicket] = db.query(model.TempTicket).filter_by(
        id=data.get("temp_ticket")).one_or_none()

    if temp_ticket is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "DATA INVALID",
                "message": "Token has some error please redo ticketing"
            },
        )

    person: Optional[model.Person] = db.query(model.Person).filter_by(
        id=temp_ticket.person).one_or_none()

    if person is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "DATA INVALID",
                "message": "Token has some error please redo ticketing"
            },
        )

    new_ticket = model.Ticket(
        match_id=temp_ticket.match_id,
        stadium_name=temp_ticket.stadium_name,
        block_name=temp_ticket.block_name,
        seat_row=temp_ticket.seat_row,
        seat_no=temp_ticket.seat_no,
        timestamps="[]",
        person=person
    )

    db.add(new_ticket)
    db.delete(temp_ticket)
    db.commit()
    db.refresh(new_ticket)

    # create email

    subject = "QRCODE"
    message = 'Here is your qrcode'

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = person.email
    msg["Subject"] = subject

    text = MIMEText(message)
    msg.attach(text)

    # create qr code
    combined_data = rsa.encrypt(
        f"{new_ticket.id}|{new_ticket.secret_id}|{new_ticket.ticket_id}".encode('utf8'), tokens.pub_key)

    qr = qrcode.QRCode(version=3, box_size=11, border=5)
    qr.add_data(combined_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_file = f"qrcodes/{new_ticket.secret_id}.png"
    img.save(img_file)

    # save qrcode to mysql

    with open(img_file, 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name="my_qr_code.png")
        msg.attach(image)

    # send email

    server.sendmail(SENDER_EMAIL, person.email, msg.as_string())

    return fastapi.responses.JSONResponse(
        content={
            "status": "DONE",
            "msg": "Ticket Created and QRCode Sent to you"
        },
        status_code=fastapi.status.HTTP_201_CREATED,
    )


# verify qr code
@router.post("/verify")
def verify_ticket(
    token: str,
    # icc=Depends(current_user),
    db: orm.Session = Depends(db_session)
):
    print(token, rsa.decrypt(bytes(token, "utf-8"), tokens.priv_key).decode('utf8'))

# resend code
