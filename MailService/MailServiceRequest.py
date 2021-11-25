from pydantic import BaseModel
from typing import Optional
class MailServiceRequest(BaseModel):
    From: dict
    To: dict
    Subject: dict
    Body: dict
    # Attachment: str