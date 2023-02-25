import fastapi
from fastapi import Depends
from smtplib import SMTPRecipientsRefused
from models.database import db_session, orm
from models import schema, model

from repository.email import Server
from repository import tokens
import qrcode

router = fastapi.APIRouter(prefix="/ticket", tags=["tickets_manager"])


@router.post("/create")
def create_ticket(new_ticket_info: schema.NewTicket, db: orm.Session = Depends(db_session)):
    person = model.Person(
        gender=new_ticket_info.gender,
        nationality=new_ticket_info.nationality,
        first_name=new_ticket_info.first_name,
        last_name=new_ticket_info.last_name,
        dob=new_ticket_info.dob,
        email=new_ticket_info.email,
        phone=new_ticket_info.phone,
    )

    # todo: add check

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
    body = f'Hi please verify you account<br>\
        <form action="https://kvkpop-fuzzy-space-goggles-5666r65jw96c759x-8080.preview.app.github.dev/ticket/generate" method="post">\
            <input type="hidden" name="token" value="{token}">\
            <input type="submit" value="Click Here">\
        </form>'

    try:
        Server().send(str(subject), str(body), str(new_ticket_info.email))

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


@router.post("/generate")
def generate_ticket(token: str = fastapi.Form(), db: orm.Session = Depends(db_session)):
    data = tokens.decrypt_token(token)
    person = db.query(model.Seat).get(1)
    # person = db.query(model.Seat).get(int(data["person_id"]))

    new_ticket = model.Ticket(
        match_id=data["match_id"],
        stadium_name=data["stadium_name"],
        block_name=data["block"],
        seat_row=data["row_name"],
        seat_no=data["seat_no"],
        person=person
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    # create qr code and send it

    subject = "QRCODE"
    body = f'Here is your qrcode<br>\
        <form action="https://kvkpop-fuzzy-space-goggles-5666r65jw96c759x-8080.preview.app.github.dev/ticket/generate" method="post">\
            <input type="hidden" name="token" value="{token}">\
            <input type="submit" value="Click Here">\
        </form>'

    try:
        Server().send(str(subject), str(body), str(person.email))
    except SMTPRecipientsRefused as exc:
        pass
