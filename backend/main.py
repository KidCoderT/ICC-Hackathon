from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import qrcode
import base64
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    '/generate_qr_code/{data}/',
    response_class=Response
)
def generate_qr_code(data: str):
    img = qrcode.make(data)
    img.save('qrcode.png')
    with open('qrcode.png', 'rb') as f:
        encoded_img = f.read()
    return Response(content=encoded_img, media_type="image/png")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
