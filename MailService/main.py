# from datetime import datetime
import os
import smtplib
# import imghdr
from email.message import EmailMessage
import urllib.request as urllib2
from email.base64mime import body_encode
import uvicorn
from fastapi import FastAPI
import logging
from pathlib import Path
# import dbAccess
from custom_logging import CustomizeLogger
from ConfigLoader import ConfigLoader
import MailService
from MailServiceRequest import MailServiceRequest
from MailServiceResponse import MailServiceResponse
from MailServiceException import MailServiceException
from loguru import logger

# for attachment
from flask import Flask, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication



# EMAIL_ADDRESS = os.environ.get('adityarachman24.ar@gmail.com')
# EMAIL_PASSWORD = os.environ.get('asificare24')
# EMAIL_HOST_USER = 'adityarachman24.ar@gmail.com'
# EMAIL_HOST_PASSWORD = 'gilfdgrwojoxciab'

config_path=Path(__file__).with_name("logging_config.json")

def create_app() -> FastAPI:
    #app = FastAPI(title='e-Form Simpanan Service', debug=False, docs_url= None, redoc_url = None)
    app = FastAPI(title='Mail Service', debug=True) #for dev only
    logger_server = CustomizeLogger.make_logger(config_path)
    app.logger = logger_server

    return app

app = create_app()
# app = Flask(__name__)

tags_metadata = [
    {
        "name": "Mail Service",
        "description": "Mail Service",
    }
]
appConfig = ConfigLoader()

@app.post('/mailservice', response_model=MailServiceResponse, response_model_exclude_unset=True)
async def mailservice(req: MailServiceRequest):
    # proxy_host = 'inet.bni.co.id'
    # proxy_port = 8080

    # timestamp = datetime.now()
    # contacts = ['madityarachman24.ar@gmail.com', 'mohamad.aditya.rachman@bni.co.id', 'cleveresta.prasetyo@bni.co.id']

    # msg = EmailMessage()
    msg = MIMEMultipart()
    msg['Subject'] = req.Subject.strip()
    msg['From'] = req.From.strip()
    msg['To'] = req.To.strip()
    msg['Body'] = req.Body.strip()
    To = msg['To']
    Body = msg['Body']
    From = msg['From']

    # msg.set_content('This is a plain text email')

    # msg.add_alternative("""\
    # <!DOCTYPE html>
    # <html>
    #     <body>
    #         <h1 style="color:SlateGray;">Ini Isi Emailnya!</h1>
    #     </body>
    # </html>
    # """, subtype='html')

    # body = 'ini is emailnyaaa'
    msgText = MIMEText('<b>%s</b>' % (Body), 'html')
    msg.attach(msgText)

    # filename = "text.txt"
    # msg.attach(MIMEText(open(filename).read()))

    with open('gambar.png', 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename="gambar.png")
        msg.attach(img)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    # 587
    # 465
    # with smtplib.SMTP_SSL(os.getenv('ENV_MAIL_HOST'), os.getenv('ENV_MAIL_PORT')) as smtp:
        # smtp.ehlo()
        smtp.starttls()
        # smtp.ehlo()
        try:
            smtp.login(From,'gilfdgrwojoxciab')
            # smtp.login(os.getenv('ENV_MAIL_USER'), os.getenv('ENV_MAIL_PASS'))
            smtp.send_message(msg)
            result = {
                "status": "Success sent Mail to "+To
            }
            smtp.quit()
        except MailServiceException as e:
            logger.info('{0}'.format(e))
            result = {
                "status": "Failed sent Mail to "+To
            }
            smtp.quit()
            raise MailServiceException("error")
        return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)