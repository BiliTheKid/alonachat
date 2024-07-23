from pydantic import BaseModel
# Define Pydantic model for request body
class TemplateRequest(BaseModel):
    name: str
    language: int
    header: int
    body: str
    buttons: int
    callToActionWebsiteText: str
    callToActionWebsiteType: int
    callToActionWebsiteText2: str
    callToActionWebsiteType2: int
