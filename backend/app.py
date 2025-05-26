from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import Adyen
from Adyen.errors import AdyenAPICommunicationError

load_dotenv()

adyen = Adyen.Adyen()
adyen.client.xapikey = os.getenv("ADYEN_API_KEY")
adyen.client.platform = os.getenv("ADYEN_ENVIRONMENT")

MERCHANT_ACCOUNT = os.getenv("ADYEN_MERCHANT_ACCOUNT")

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Adyen Drop-in Demo Backend is running!"})

if __name__ == '__main__':
    app.run(debug=True)
