from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
import os
from dotenv import load_dotenv
import Adyen
from Adyen.exceptions import AdyenError
import random
import uuid

load_dotenv()

app = Flask(__name__)
# CORS(app)

adyen = Adyen.Adyen()
adyen.client.platform = os.getenv("ADYEN_ENVIRONMENT")
adyen.client.xapikey = os.getenv("ADYEN_API_KEY")

MERCHANT_ACCOUNT = os.getenv("ADYEN_MERCHANT_ACCOUNT")
CLIENT_KEY = os.getenv("ADYEN_CLIENT_KEY")

@app.route("/api/sessions", methods=["POST"])
def create_checkout_session():
    try:
        payload = {
            "merchantAccount": MERCHANT_ACCOUNT,
            "amount": {
                "currency": "EUR",
                "value": 1000
            },
            "reference": f"ORD-{random.randint(10000000, 99999999)}",
            "returnUrl": "http://localhost:8080/checkout",
            "countryCode": "NL",
            "lineItems": [{"quantity": 1, "amountIncludingTax": 5000, "description": "Sunglasses"}]
        }

        session = adyen.checkout.payments_api.sessions(
            request=payload,
            idempotency_key=str(uuid.uuid4())
        )
        return jsonify(session.message)

    except AdyenError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/checkout")
def checkout():
    return render_template("checkout.html", client_key=CLIENT_KEY)

@app.route("/")
def index():
    return '<a href="/checkout">Go to Checkout</a>'


if __name__ == "__main__":
    app.run(debug=True, port=8080)
