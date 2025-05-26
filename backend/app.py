from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import Adyen
from Adyen.exceptions import AdyenError
import random

load_dotenv()

app = Flask(__name__)

adyen = Adyen.Adyen()
adyen.client.platform = os.getenv("ADYEN_ENVIRONMENT")
adyen.client.xapikey = os.getenv("ADYEN_API_KEY")

MERCHANT_ACCOUNT = os.getenv("ADYEN_MERCHANT_ACCOUNT")

@app.route("/api/sessions", methods=["POST"])
def create_checkout_session():
    try:
        payload = {
            "merchantAccount": MERCHANT_ACCOUNT,
            "amount": {
                "currency": "USD",
                "value": 1000
            },
            "reference": f"ORD-{random.randint(10000000,99999999)}",
            "returnUrl": "http://localhost:3000/returnurl",
            "countryCode": "US"
        }

        result = adyen.checkout.payments_api.sessions(
            request=payload,
            idempotency_key="UUID"
        )

        return jsonify(result.message)

    except AdyenError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
