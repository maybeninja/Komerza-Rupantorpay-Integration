import requests

from config import *
from payments import (
    get_payment,
    save_payment,
    payment_expired,
)

CHECKOUT_URL = "https://payment.rupantorpay.com/api/payment/checkout"
VERIFY_URL = "https://payment.rupantorpay.com/api/payment/verify-payment"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": RupantarPayAPIKey,
}


def create_payment(
    orderid: str,
    email: str,
    amount_eur: float,
    amount_bdt: float,
):
    """
    Creates a new RupantorPay payment.

    If a pending payment already exists and hasn't expired,
    the existing payment URL is returned instead.
    """

    cached = get_payment(orderid)

    if (
        cached
        and cached["status"] == "PENDING"
        and not payment_expired(orderid)
        and cached.get("payment_url")
    ):
        return {
            "success": True,
            "cached": True,
            "payment_url": cached["payment_url"],
        }

    payload = {
        "success_url": f"https://checkout.komerza.com/checkout/{orderid}",
        "cancel_url": f"{BaseURL}/{orderid}/cancel",
        "webhook_url": f"{BaseURL}/webhook/{orderid}/paid",
        "fullname": orderid,
        "email": email,
        "amount": amount_bdt,
    }

    try:
        response = requests.post(
            CHECKOUT_URL,
            json=payload,
            headers=HEADERS,
            timeout=20,
        )
    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e),
        }

    if not response.ok:
        return {
            "success": False,
            "error": response.text,
        }

    data = response.json()

    payment_url = data.get("payment_url")

    if not payment_url:
        return {
            "success": False,
            "error": "payment_url missing from response.",
        }

    save_payment(
        orderid=orderid,
        payment_url=payment_url,
        amount_eur=amount_eur,
        amount_bdt=amount_bdt,
    )

    return {
        "success": True,
        "cached": False,
        "payment_url": payment_url,
    }


def verify_payment(transaction_id: str):
    payload = {
        "transaction_id": transaction_id,
    }

    try:
        response = requests.post(
            VERIFY_URL,
            json=payload,
            headers=HEADERS,
            timeout=20,
        )
    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e),
        }

    if not response.ok:
        return {
            "success": False,
            "error": response.text,
        }

    data = response.json()

    required = [
        "status",
        "fullname",
        "email",
        "amount",
        "payment_method",
        "transaction_id",
    ]

    for field in required:
        if field not in data:
            return {
                "success": False,
                "error": f"Missing '{field}' in verify response.",
            }

    return {
        "success": True,
        "transaction_id": data["transaction_id"],
        "fullname": data["fullname"],
        "email": data["email"],
        "amount": float(data["amount"]),
        "payment_method": data["payment_method"],
        "status": data["status"].upper(),
        "raw": data,
    }