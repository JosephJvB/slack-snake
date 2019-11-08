import os
import slack

if not os.environ["BOT_TOKEN"]:
    print("NO BOT TOKEN FOUND")
    print("Exiting...")
else:
    client = slack.WebClient(token=os.environ["BOT_TOKEN"])
    response = client.chat_postMessage(
        channel='#general',
        text="Hello world!")