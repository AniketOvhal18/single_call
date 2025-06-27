
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import google.generativeai as genai
import os

app = Flask(__name__)

# Twilio Credentials from environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")
my_number = os.environ.get("MY_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Start chat session with system prompt
chat = model.start_chat(history=[
    {
        "role": "system",
        "parts": [
            """You are Gaytri from Kumar Properties, a polite and helpful AI real estate calling assistant.
You are calling to understand the client’s property requirements.
Ask questions one at a time, wait for the user’s response, then continue.
Your goal is to collect:
- Number of BHKs required
- Preferred location or area
- Budget range
- Type of property (Flat, Villa, Commercial, etc.)
- Purpose (Investment, Self-use, Rental)
- Any other specific requirement
Be brief, conversational, and never robotic.
Start with a friendly greeting."""
        ]
    }
])

@app.route("/")
def home():
    return "✅ Real Estate AI Calling Bot is running."

@app.route("/make_call", methods=["GET"])
def make_call():
    call = client.calls.create(
        to=my_number,
        from_=twilio_number,
        url="https://your-app.onrender.com/voice"  # Change after deployment
    )
    return f"📞 Call initiated. SID: {call.sid}"

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/process_speech', method='POST', timeout=5)
    gather.say("Hi! This is Gaytri from Kumar Properties. I'm here to help you find the right property. May I ask a few questions to understand your requirements?")
    response.append(gather)
    response.redirect('/voice')  # Repeats if no speech input
    return Response(str(response), mimetype='text/xml')

@app.route("/process_speech", methods=["POST"])
def process_speech():
    user_input = request.form.get('SpeechResult', '')

    if not user_input:
        twiml = VoiceResponse()
        twiml.say("Sorry, I didn’t catch that. Let’s try again.")
        twiml.redirect('/voice')
        return Response(str(twiml), mimetype='text/xml')

    try:
        gemini_reply = chat.send_message(user_input).text
    except Exception as e:
        gemini_reply = "I'm sorry, something went wrong while processing your response."

    response = VoiceResponse()
    gather = Gather(input='speech', action='/process_speech', method='POST', timeout=5)
    gather.say(gemini_reply)
    response.append(gather)
    response.redirect('/voice')  # Keep looping
    return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)

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
