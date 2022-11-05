from fastapi import FastAPI, Request
import httpx 
import os
from google.cloud import dialogflow_v2 as dialogflow

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    message = await request.json()
    chat_id = message['message']['from']['id']
    message_receive = message['message']['text']
    text = '¡Bienvenido!'
    url = "https://api.telegram.org/bot5432978209:AAGmcszR6u_QBIbD9cFtp6QC3QSMIV6IYsY/sendMessage"

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ga.json"

    client = dialogflow.SessionsClient()
    session = client.session_path(project="carbon-gecko-367717", session="me")
    text_input = dialogflow.TextInput(text= message_receive, language_code = "es")
    query_input = dialogflow.QueryInput(text = text_input)
    response = client.detect_intent(query_input=query_input, session=session)

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, json={"chat_id": chat_id, "text": response.query_result.fulfillment_text})
        
        
    return message