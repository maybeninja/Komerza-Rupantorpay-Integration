import json
import os
import time

PAYMENTS_FILE = "payment.json"


def _ensure():
    if not os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "orders": {},
                    "transactions": {}
                },
                f,
                indent=4
            )


def load():
    _ensure()

    try:
        with open(PAYMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "orders": {},
            "transactions": {}
        }


def save(data):
    with open(PAYMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_payment(orderid):
    data = load()
    return data["orders"].get(orderid)


def get_payment_from_transaction(transaction_id):
    data = load()

    orderid = data["transactions"].get(transaction_id)

    if not orderid:
        return None

    return data["orders"].get(orderid)


def save_payment(
    orderid,
    payment_url,
    amount_eur,
    amount_bdt
):
    data = load()

    data["orders"][orderid] = {
        "payment_url": payment_url,
        "transaction_id": None,
        "payment_method": None,
        "status": "PENDING",
        "amount_eur": amount_eur,
        "amount_bdt": amount_bdt,
        "created_at": int(time.time()),
        "completed_at": None
    }

    save(data)


def update_payment(orderid, **kwargs):
    data = load()

    if orderid not in data["orders"]:
        return False

    data["orders"][orderid].update(kwargs)

    transaction_id = kwargs.get("transaction_id")

    if transaction_id:
        data["transactions"][transaction_id] = orderid

    save(data)
    return True


def delete_payment(orderid):
    data = load()

    payment = data["orders"].get(orderid)

    if payment:
        transaction_id = payment.get("transaction_id")

        if transaction_id:
            data["transactions"].pop(transaction_id, None)

        data["orders"].pop(orderid, None)

        save(data)


def payment_exists(orderid):
    return get_payment(orderid) is not None


def payment_completed(orderid):
    payment = get_payment(orderid)

    if not payment:
        return False

    return payment["status"] == "COMPLETED"


def payment_expired(orderid, expiry=900):
    payment = get_payment(orderid)

    if not payment:
        return True

    if payment["status"] != "PENDING":
        return True

    return (time.time() - payment["created_at"]) > expiry