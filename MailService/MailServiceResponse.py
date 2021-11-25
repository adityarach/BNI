from pydantic import BaseModel
from typing import Optional
class MailServiceResponse(BaseModel):
    status: Optional[str] = None