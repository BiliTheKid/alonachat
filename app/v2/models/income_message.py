from pydantic import BaseModel
# Define the model for incoming messages
class IncomingMessage(BaseModel):
    status: str
    from_number: str
    to: str
    sender_name: str
    type: str
    body: str
    media: bool
    timestamp: str

    class Config:
        allow_population_by_field_name = True
        fields = {
            'from_number': 'from',
            'sender_name': 'senderName'
        }
