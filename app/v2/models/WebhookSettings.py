from pydantic import BaseModel

class WebhookSettings(BaseModel):
    apiKey: str
    from_number: str
    url: str = " "
    system: int = 0
    systemPhoneAlert: str = " "
