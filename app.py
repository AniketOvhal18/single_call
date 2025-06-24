from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os

app = Flask(__name__)

# Set your credentials directly or use environment variables from Render
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")
my_number = os.environ.get("MY_PHONE_NUMBER")

client = Client(account_sid, auth_token)

@app.route("/")
def home():
    return "Flask Call App Running!"

@app.route("/make_call", methods=["GET"])
def make_call():
    call = client.calls.create(
        to=my_number,
        from_=twilio_number,
        url="https://your-app.onrender.com/voice"  # Update this after deployment
    )
    return f"Call initiated. SID: {call.sid}"

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say("Hello! This is a test call from your Flask app hosted on Render.")
    return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
