from typing import Any, Dict
from fastapi.responses import JSONResponse
from prisma import Prisma
from prisma.models import OptionalAnswer
import logging
from fastapi import FastAPI, HTTPException, Request
# from  app.v2.setup.OptionalAnswer import  optional_answer_crud 
from dotenv import load_dotenv
import requests
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from httpx import AsyncClient, request
import os
import re 
load_dotenv()
from models.user import UserState
from helpers.helpers import send_message_non , get_template_sender , TemplateSender , send_message_gen, send_message_name_hotel, get_message_sender, send_message_name_identification, send_message_name_id, send_message_place, send_message_ppl
# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



####
# Initialize FastAPI app
app = FastAPI()
# Initialize Prisma
db = Prisma(auto_register=True)
@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


## regex for general questions checking
COMMANDS = {
    'TEXT': re.compile(r' הי| שלום| היי| מה קורה? אהלן'),
}

user_states = {}

response_options = {
    'abroad': 'חול',
    'base': 'בסיס',
    'apartment': 'דירה',
    'hotel': 'מלון',
    'settlement': 'יישוב',
    'other': 'אחר',
    'yes': 'כן',
    'no': 'לא'
}

question_text = "תשובה לשאלה היכן אתה:"


def extract_and_map_fields(data: dict[str, Any]) -> Dict[str, Any]:
    mapped_data = {
        "status": data.get('status', ''),
        "from_number": data.get('from', ''),
        "to": data.get('to', ''),
        "sender_name": data.get('senderName', ''),
        "type": data.get('type', ''),
        "body": data.get('body', ''),
        "media": data.get('media', False),
        "timestamp": data.get('timestamp', '')
    }
    return mapped_data

def get_user_state(user_id: str) -> UserState:
    if user_id not in user_states:
        user_states[user_id] = UserState(user_id)
    return user_states[user_id]

 
@app.post("/")
async def receive_message(request: Request):
    # Receive and process the data
    data = await request.json()
    print(data)

    # Extract and map fields
    incoming_message = extract_and_map_fields(data)
    print("Extracted fields:", incoming_message)

    ## edit
    if incoming_message.get("body"):
        user_id = incoming_message.get('from_number')
        user_state = get_user_state(user_id)
        print(f"User ID: {user_id}")
        print(f"User State: {user_state}")
        
        # Handle state transition with non-empty body
        response_message = handle_transition(user_state, incoming_message)

    else:
        print("Received empty message body. Skipping processing.")

    ## check if the system numer not send itslef
    # if incoming_message.get('from') != incoming_message.get('to'):
    #         # check number and message exist 
    #         if incoming_message.get('from_number') and incoming_message.get("body"):
    #                 print("send message --  ")
    #                 send_message(incoming_message)


    # ## in-process dont touch! 
    # for message in data.get('messages', []):
    #         if not message.get('from_me'):  # Only process messages not sent by the user
    #             #chat_id = message.get('chat_id').split('@')[0]  # Extracting phone number from chat_id
    #             chat_id = message.get('from_number')
    #             text = message.get('text')
    #             print(chat_id,text )
                # from_user = message.get('from', {})
                # print(f"Received message from {from_user}: {text}")
                
                # if chat_id and text:
                #     send_message(from_user, text)  # Call send_message only if conditions are met
                
    return JSONResponse(content=incoming_message, status_code=200)

def handle_transition(user_state: UserState, user_input: dict) -> str:
    current_stage = user_state.get_current_stage()
    print(f"Current stage: {current_stage}")

    user_response = user_input.get("body")
    print(f"User response: {user_response}")

    if current_stage == 'start':
        user_state.update_state('identification')
        # sender = get_template_sender("start")      
        #response = sender.send_template(user_input) 
        message_sender = get_message_sender("identification")  # Create the appropriate sender instance
        response = send_message_name_identification(user_input.get("to"),user_input.get("from_number"))  # Send the template


    elif current_stage == 'Legal_confirmation':
        if user_response in ['כן', 'לא']:
            user_state.update_data('Legal_confirmation_approved', user_response == 'כן')
            print(f"מאשר לנו לשמור את פרטיו האיישים: {user_response == 'כן'}")
            if user_response == 'כן':
                print("Updating state to collecting_basic_info")
                user_state.update_state('collecting_basic_info')
                sender = get_template_sender("collecting_basic_info")  # Create the appropriate sender instance
                response = sender.send_template(user_input)  # Send the template
            else:
                user_state.update_state('END')
                # user_state.update_data('Legal_confirmation_decline', user_response == 'לא')
                send_message_non(user_input.get("to"),user_input.get("from_number"))
                # user_state.update_state('Legal_confirmation_decline')
                # message_sender = get_message_sender("END")
                # response = message_sender.send_message(user_input)
                # user_state.update_state('END')
                
        else:
                user_state.update_state('input_mistake')
                send_message_gen(user_input.get("to"),user_input.get("from_number"))

    elif current_stage == 'collecting_basic_info':
        user_state.update_data('collecting_basic_info', user_response)
        print(f"תשובה לשאלה היכן אתה: {user_response}")
        if user_response in ['חול', 'בסיס', 'דירה', 'מלון', 'יישוב', 'אחר']:
            user_state.update_data('current_location', user_response)
            if user_response == 'מלון':
                user_state.update_state('hotel')
                # message_sender = get_message_sender("hotel")  # Create the appropriate sender instance
                #response = send_message_name_hotel(user_input.get("to"),user_input.get("from_number"))  # Send the template
                message_sender = get_message_sender("hotel")
                response = message_sender.send_message(user_input)
            
            if user_response == 'יישוב':
                user_state.update_state('settlements')
                # message_sender = get_message_sender("hotel")  # Create the appropriate sender instance
                #response = send_message_name_hotel(user_input.get("to"),user_input.get("from_number"))  # Send the template
                sender = get_template_sender("settlements")
                response = sender.send_template(user_input)            
            
            if user_response == 'דירה':
                user_state.update_state('apartment')
                # message_sender = get_message_sender("hotel")  # Create the appropriate sender instance
                #response = send_message_name_hotel(user_input.get("to"),user_input.get("from_number"))  # Send the template
                message_sender = get_message_sender("apartment")
                response = message_sender.send_message(user_input)            
            
            if user_response == 'אחר':
                user_state.update_state('collecting_basic_info_other')
                # message_sender = get_message_sender("hotel")  # Create the appropriate sender instance
                #response = send_message_name_hotel(user_input.get("to"),user_input.get("from_number"))  # Send the template
                message_sender = get_message_sender("collecting_basic_info_other")
                response = message_sender.send_message(user_input)           


            
            # else:
            #     user_state.update_state('input_mistake')
            #     send_message_gen(user_input.get("to"),user_input.get("from_number"))

        # user_state.update_state('ASKING_SPECIFIC_QUESTIONS')
        # return f"Nice to meet you, {user_response}. What brings you here today?"
    
    elif current_stage == 'identification':
        user_state.update_data('id_number', user_response)
        # print(f" מה מס תז שלך? {user_response} היי, ")
        # message_sender = get_message_sender("identification")
        send_message_name_id(user_input.get("to"),user_input.get("from_number"),user_response)
        # response = message_sender.send_message(user_input)
        user_state.update_state('id_number')

    elif current_stage == 'id_number':
        user_state.update_data('id_number', user_response)
        send_message_place(user_input.get("to"),user_input.get("from_number"))
        # user_state.update_state('children_exist')
        user_state.update_state('place')

    elif current_stage == 'place':
        user_state.update_data('place', user_response)
        send_message_ppl(user_input.get("to"),user_input.get("from_number"))
        # user_state.update_state('children_exist')
        user_state.update_state('place')

    elif current_stage == 'collecting_basic_info_other':
        user_state.update_data('collecting_basic_info_other', user_response)
        print(f"תשובה לשאלה פתוחה(אחר): {user_response}")
        user_state.update_state('children_exist')
    # elif current_stage == 'ASKING_SPECIFIC_QUESTIONS':
    #     user_state.update_data('purpose', user_response)
    #     if user_response.lower() == 'support':
    #         user_state.update_state('ASKING_SUPPORT_QUESTIONS')
    #         return "Can you describe your issue?"
    #     else:
    #         user_state.update_state('PROVIDING_RECOMMENDATIONS')
    #         return "Do you prefer A or B?"
    
    # elif current_stage == 'ASKING_SUPPORT_QUESTIONS':
    #     user_state.update_data('issue', user_response)
    #     user_state.update_state('PROVIDING_RECOMMENDATIONS')
    #     return "Thank you for the details. Based on your issue, I recommend XYZ. Is there anything else I can help you with?"
    
    # elif current_stage == 'PROVIDING_RECOMMENDATIONS':
    #     user_state.update_data('preference', user_response)
    #     user_state.update_state('CONCLUSION')
    #     return "Based on your answers, I recommend XYZ. Is there anything else I can help you with?"
    
    # elif current_stage == 'CONCLUSION':
    #     return "Thank you for chatting with us. Have a great day!"
    
    elif current_stage == 'END':
        return "Thank you. Have a nice day!"


## maped option based on user response prevent hebrew issues.
# def handle_transition(user_state: UserState, user_input: dict) -> str:
#     current_stage = user_state.get_current_stage()
#     print(f"Current stage: {current_stage}")

#     user_response = user_input.get("body")
#     print(f"User response: {user_response}")

#     if current_stage == 'start':
#         user_state.update_state('Legal_confirmation')
#         sender = get_template_sender("start")
#         response = sender.send_template(user_input)

#     elif current_stage == 'Legal_confirmation':
#         if user_response in response_options.values():  # Check if the response is valid
#             if user_response == response_options['yes']:
#                 user_state.update_data('Legal_confirmation_approved', True)
#                 print(f"מאשר לנו לשמור את פרטיו האישים: True")
#                 print("Updating state to collecting_basic_info")
#                 user_state.update_state('collecting_basic_info')
#                 sender = get_template_sender("collecting_basic_info")
#                 response = sender.send_template(user_input)
#             elif user_response == response_options['no']:
#                 user_state.update_data('Legal_confirmation_approved', False)
#                 print(f"מאשר לנו לשמור את פרטיו האישים: False")
#                 user_state.update_state('END')
#                 send_message_non(user_input.get("to"), user_input.get("from_number"))
#         else:
#             user_state.update_state('input_mistake')
#             send_message_gen(user_input.get("to"), user_input.get("from_number"))

#     elif current_stage == 'collecting_basic_info':
#         user_state.update_data('collecting_basic_info', user_response)
#         print(f"{question_text} {user_response}")

#         for key, value in response_options.items():
#             if user_response == value:
#                 user_state.update_data('current_location', user_response)
                
#                 if key == 'hotel':
#                     user_state.update_state('hotel')
#                     message_sender = get_message_sender("hotel")
#                     response = message_sender.send_message(user_input)
                
#                 elif key == 'settlement':
#                     user_state.update_state('settlements')
#                     sender = get_template_sender("settlements")
#                     response = sender.send_template(user_input)
                
#                 elif key == 'apartment':
#                     user_state.update_state('apartment')
#                     message_sender = get_message_sender("apartment")
#                     response = message_sender.send_message(user_input)
                
#                 elif key == 'other':
#                     user_state.update_state('collecting_basic_info_other')
#                     message_sender = get_message_sender("collecting_basic_info_other")
#                     response = message_sender.send_message(user_input)
                
#                 break
#         else:
#             user_state.update_state('input_mistake')
#             send_message_gen(user_input.get("to"), user_input.get("from_number"))

#     elif current_stage == 'hotel':
#         user_state.update_data('hotel', user_response)
#         print(f"תשובה לשאלה באיזה מלון אתה שוהה: {user_response}")
#         user_state.update_state('children_exist')

#     elif current_stage == 'apartment':
#         user_state.update_data('apartment', user_response)
#         print(f"תשובה לשאלה באיזה דירה אתה שוהה: {user_response}")
#         user_state.update_state('children_exist')

#     elif current_stage == 'collecting_basic_info_other':
#         user_state.update_data('collecting_basic_info_other', user_response)
#         print(f"תשובה לשאלה פתוחה(אחר): {user_response}")
#         user_state.update_state('children_exist')

#     elif current_stage == 'END':
#         return "Thank you. Have a nice day!"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)