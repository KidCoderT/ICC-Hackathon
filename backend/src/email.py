import os
import smtplib

SENDER_EMAIL_PASSWORD = str(os.getenv("SENDER_EMAIL_PASSWORD"))
SENDER_EMAIL = str(os.getenv("SENDER_EMAIL"))

# class Server(metaclass=SingletonMeta):
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     sender = ""

#     @staticmethod
#     def initialize(email, password):
#         Server.server.starttls()
#         Server.server.login(email, password)
#         Server.sender = email

#     def send(self, subject: str, body: str, receiver: str) -> bool:
#         try:
#             message = generate_mail(subject, body, self.sender, receiver)
#             self.server.sendmail(self.sender, receiver, message)
#         except smtplib.SMTPRecipientsRefused as exc:
#             raise ValueError("Your email address is invalid!!") from exc

#         return True


# def generate_mail(subject: str, body: str, from_add: str, to_add: str):
#     msg = MIMEText(body, "html")
#     msg["Subject"] = subject
#     msg["From"] = from_add
#     msg["To"] = to_add

#     return msg.as_string()

def smtp_server():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        yield server
