from smtplib import SMTPRecipientsRefused, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import qrcode
import fastapi
from fastapi import Depends

from models.database import db_session, orm
from models import schema, model

from src.email import smtp_server, SENDER_EMAIL
from src import tokens

router = fastapi.APIRouter(prefix="/ticket", tags=["tickets_manager"])


@router.post("/create")
def create_ticket(new_ticket_info: schema.NewTicket, server: SMTP_SSL = Depends(smtp_server), db: orm.Session = Depends(db_session)):
    person = model.Person(
        gender=new_ticket_info.gender,
        nationality=new_ticket_info.nationality,
        first_name=new_ticket_info.first_name,
        last_name=new_ticket_info.last_name,
        dob=new_ticket_info.dob,
        email=new_ticket_info.email,
        phone=new_ticket_info.phone,
    )

    # todo: check if stadium present
    # todo: check if block present
    # todo: check if seat present
    # todo: check if seat not taken

    db.add(person)
    db.commit()
    db.refresh(person)

    token_data = {
        "person_id": person.id,
        "match_id": new_ticket_info.match_id,
        "stadium_name": new_ticket_info.stadium_name,
        "block": new_ticket_info.block,
        "row_name": new_ticket_info.row_name,
        "seat_no": new_ticket_info.seat_no,
    }

    token = tokens.create_access_token(token_data)

    subject = "verify token"
    message = f'Hi please verify you account<br>\
        <form action="https://kvkpop-vigilant-journey-x5rxvxv447vfv5qg-8080.preview.app.github.dev/ticket/generate" method="post">\
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
    data = tokens.decrypt_token(token)
    person = db.query(model.Person).get(int(data["person_id"]))

    new_ticket = model.Ticket(
        match_id=data["match_id"],
        stadium_name=data["stadium_name"],
        block_name=data["block"],
        seat_row=data["row_name"],
        seat_no=data["seat_no"],
        timestamps="[]",
        person=person
    )

    # verify_info

    db.add(new_ticket)
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

    combined_data = f"{new_ticket.id}|{new_ticket.secret_id}|{new_ticket.ticket_id}"
    # ENCODE

    qr = qrcode.QRCode(version=3, box_size=11, border=5)
    qr.add_data(combined_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_file = f"qrcodes/{new_ticket.ticket_id}.png"
    img.save(img_file)

    # attach_qrcode

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
