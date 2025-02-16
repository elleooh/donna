# Prerequisites

To use the app, you will need:

Python version: `3.9.13`
- **A Twilio account.** You can sign up for a free trial [here](https://www.twilio.com/try-twilio).
- **A Twilio number with _Voice_ capabilities.** [Here are instructions](https://help.twilio.com/articles/223135247-How-to-Search-for-and-Buy-a-Twilio-Phone-Number-from-Console) to purchase a phone number.
- **An OpenAI account and an OpenAI API Key.** You can sign up [here](https://platform.openai.com/).
  - **OpenAI Realtime API access.**
- **ngrok** for tunneling local server to the internet

# Inbound Call
## Start the server
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --service inbound
```
## Start ngrok
```
ngrok http 5050
```
## Update the ngrok URL in the Twilio console
 See instructions [here](https://www.twilio.com/en-us/blog/voice-ai-assistant-openai-realtime-api-python)

## Make a call to your Twilio number

# Outbound Call
## Start the server
```
python main.py --service outbound --call YOUR_OWN_NUMBER
```
You will receive a call from your Twilio number so pick it up and say hi!
