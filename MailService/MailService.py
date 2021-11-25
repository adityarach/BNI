import os
from string import Template
import requests
from MailServiceException import MailServiceException
from loguru import logger
import json

from email.base64mime import body_encode

url = os.getenv('ENV_LIVENESS_V2_ENDPOINT')

def mailService(To, Subject):

    body = """{
        "From" : "${From}",
        "Subject" : "${Subject}"
    }"""

    t = Template(body)
    req=t.safe_substitute(To=To, Subject=Subject)

    header = {"Content-type": "application/json"}

    x = requests.post(url, data = req, headers=header)
    print(x)
    y = x.text
    datas = json.loads(y)
    logger.info(datas)

    # From = datas["From"]
    To = datas["To"]
    Subject = datas["Subject"]

    res_mail = {
        # 'From':From,
        'To':To,
        'Subject':Subject
    }

    return res_mail
