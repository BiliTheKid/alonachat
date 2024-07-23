
# @app.post("/setWebhook")
# async def set_webhook(settings: WebhookSettings):
#     webhook_url = "https://api.99digital.co.il/whatsapp/v2/setWebhook"
    
#     # Prepare the payload
#     payload = {
#         "apiKey": settings.apiKey or os.getenv("API_KEY"),
#         "from": settings.from_number or os.getenv("PHONE"),
#         "url": settings.url or os.getenv("URL"),
#         "system": settings.system,
#         "systemPhoneAlert": settings.systemPhoneAlert
#     }

#     # Send the POST request
#     response = requests.post(webhook_url, json=payload)

#     if response.status_code == 200:
#         return {"message": "Webhook set successfully."}
#     else:
#         raise HTTPException(status_code=response.status_code, detail=response.text)
