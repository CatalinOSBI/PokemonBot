import requests
import os
from dotenv import load_dotenv

load_dotenv()

def phone_alert():
  response = requests.post(os.getenv('WEBHOOK_URL'))
  print(f"RESPONSE: {response}")

# Leave this here for testing
if __name__ == "__main__":
    phone_alert()
