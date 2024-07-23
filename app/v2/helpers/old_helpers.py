
# def send_message(incoming_message):
#     try:
#         sender_name = (incoming_message.get("sender_name"))
#         print(sender_name)
#         print(incoming_message.get("from_number"))
#         COMMAND_MESSAGES = {
#         r'TEXT': f' הי {sender_name} , האם תרצי להתפנות לאתר אוהלים?'
#         }
#         print(COMMAND_MESSAGES)
        
#         command= None
#         print(command)
#                 # Check if text is a string
#         if isinstance(incoming_message.get("body"), str):
#             # Initial command matching using regex patterns
#             for cmd, pattern in COMMANDS.items():
#                 print(incoming_message.get("body"))
#                 if pattern.search(incoming_message.get("body")):
#                     command = cmd
#                     break

#         if command:
#             print("cpmmand")
#             response_message = COMMAND_MESSAGES.get(command, "Default response message.")
#             print(f"Response message -> {response_message}")
#             success = send_template_endpoint(incoming_message)
#             print(success)
#             if success:
#                     print(f"Message sent: {response_message}")
#             else:
#                     print(f"Failed to send message: {response_message}")
#     except Exception as e:
#         print(f"Error in send_message: {e}")

# Endpoint to create template
# @app.post("/create_template")
# async def create_template(template_data: TemplateRequest):
#     url = "https://api.99digital.co.il/whatsapp/v2/createTemplate"

#     # Construct payload
#     payload = {
#         "apiKey": os.getenv("API_KEY"),
#         "from": "972543502375",
#         "name": template_data.name,
#         "language": template_data.language,
#         "header": template_data.header,
#         "body": template_data.body,
#         "buttons": template_data.buttons,
#         "callToActionWebsiteText": template_data.callToActionWebsiteText,
#         "callToActionWebsiteType": template_data.callToActionWebsiteType,
#         "callToActionWebsiteText2": template_data.callToActionWebsiteText2,
#         "callToActionWebsiteType2": template_data.callToActionWebsiteType2
#     }

#     # Construct headers
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "authorization": f"Bearer {os.getenv('API_KEY')}"
#     }





#     # async with AsyncClient() as client:
#     #     # Make async POST request
#     #     response = await client.post(url, json=payload, headers=headers)

#     # # Check response status
#     # if response.status_code != 200:
#     #     raise HTTPException(status_code=response.status_code, detail=response.text)

#     # return {"message": "Template creation successful", "response": response.json()}

# def send_question(api_key, from_number, to_number, name, language, header_type):
#     api_99 = os.getenv("API_BRIDGE")  # Replace with your actual API endpoint
#     #url = os.getenv("API_BRIDGE")  # Replace with your actual API endpoint
#     suffix = "/sendTemplate"    # The suffix you want to add
#     url = api_99 + suffix
    
#     payload = {
#         "apiKey": api_key ,
#         "from": from_number,
#         "to": to_number,
#         "name": name,
#         "language": language,
#         "headerType": header_type
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     print(payload)
#     response = requests.post(url, json=payload, headers=headers)
#     print(response)
#     if response.status_code == 200:
#         return {"message": "Question sent successfully."}
#     else:
#         raise HTTPException(status_code=response.status_code, detail=response.text)

# def send_template_endpoint(incomingMessage: IncomingMessage):
#     """
#     this fuction not finshed yet, depnds on the db. 
#     "apiKey": "xxxxxxxx",
#     "from": "972xxxxxx",
#     "to": "972xxxx",
#     "name": "website_welcome_he",
#     "language": 1, # hebrew defined as 1 , english 2, harbic 3 ...
#     "headerType":1 # depends on the media none, pic, doc etc
# }  
#     """
#     print("send_template_endpoint ----------")
#     api_key = os.getenv("API_KEY")
#     from_number = os.getenv("PHONE")
#     to_number =  incomingMessage.get("from_number")
#     name = "website_welcome_he"
#     language = 1
#     header_type = 1
#     return send_question(api_key, from_number, to_number, name, language, header_type)
