import requests

from config import *

BASE_URL = f"https://api.komerza.com/stores/{KomerzaStoreID}"

HEADERS = {
    "Authorization": f"Bearer {KomerzaAPIKey}"
}


def _request(method, endpoint, **kwargs):
    try:
        response = requests.request(
            method=method,
            url=BASE_URL + endpoint,
            headers=HEADERS,
            timeout=20,
            **kwargs,
        )
    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

    if not response.ok:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

    try:
        return {
            "success": True,
            "data": response.json()
        }
    except Exception:
        return {
            "success": False,
            "error": "Invalid JSON response."
        }


def get_order(orderid):
    response = _request(
        "GET",
        f"/orders/{orderid}"
    )

    if not response["success"]:
        return response

    body = response["data"]

    if not body.get("success"):
        return {
            "success": False,
            "error": "Order not found."
        }

    return {
        "success": True,
        "order": body["data"]["order"]
    }


def deliver_order(orderid):
    return _request(
        "PUT",
        f"/orders/{orderid}/deliver"
    )


def order_exists(orderid):
    return get_order(orderid)["success"]


def is_delivered(order):
    return (
        order.get("status") == "Delivered"
        or order.get("isDeliveredManually", False)
    )


def get_email(order):
    return order["customer"]["emailAddress"]


def get_amount(order):
    return float(order["amount"])


def get_currency(order):
    return order["currencyCode"]


def get_status(order):
    return order["status"]


def get_customer(order):
    return order["customer"]


def get_gateway(order):
    return order["gateway"]


def get_order_id(order):
    return order["id"]