import os
from fastapi import FastAPI, status, HTTPException, Body
from fastapi.openapi.utils import get_openapi
from typing import Dict
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi import SlackRequestHandler
import openai

app = FastAPI()

openai.api_key = os.environ.get("OPENAI_TOKEN")
openai_engine = "gpt-3.5-turbo"

slack_app = AsyncApp(token=os.environ.get("SLACK_APP_TOKEN"))

handler = SlackRequestHandler(slack_app)


@app.on_event("startup")
async def startup_event():
    app.openapi_schema = None


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_schema():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ChatGPT API",
        version="0.1.0",
        description="API for interacting with OpenAI's GPT-3 chatbot",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.post("/pangpt/decryption/")
async def decryption_message_receiver(body: Dict[str, str] = Body(...)):
    request = """
    I want you to role play as a bot that specializes within the network and cybersecurity industry, specifically with Palo Alto Networks PAN-OS firewalls.
    You will be fed a JSON formatted log message from the firewall and will be tasked with troubleshooting the decryption log below.
    Your response will be detailed troubleshooting information. Include affected users, affected devices, and any other information that would be helpful to the user.
    Your response will not reference yourself, will be without pronouns, and will be written in the third person as a Slack message.
    The response needs to be structured in Slack Block format as it will be sent to the user as a Slack message.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{request}."},
                {"role": "user", "content": f"{body}"},
            ],
        )
        message = response.choices[0]["message"]
        print(message)
        msg = message.to_dict_recursive()
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": msg["content"]},
            }
        ]
        await slack_app.client.chat_postMessage(
            channel=os.environ.get("SLACK_CHANNEL"),
            blocks=blocks,
            token=os.environ.get("SLACK_BOT_TOKEN"),
        )
        return status.HTTP_200_OK
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
