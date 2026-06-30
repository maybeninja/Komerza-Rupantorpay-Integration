# Komerza × RupantorPay Integration

A lightweight FastAPI integration that connects **Komerza Custom Payments** with **RupantorPay** for automatic payment verification and order delivery.

## Features

* Automatic RupantorPay checkout
* Live EUR → BDT conversion
* Payment verification
* Automatic Komerza order delivery
* Discord payment notifications
* Payment session caching

## Requirements

* Python 3.10+
* See `requirements.txt`

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure `settings.yml` with your:

   * Komerza API Key
   * Komerza Store ID
   * RupantorPay API Key
   * Base URL
   * Discord Webhook URL

3. Create a **Custom Payment Method** in your Komerza dashboard (e.g. **bKash** or **Nagad**).

4. Set the **Redirect URL** to:

```text
{BASE_URL}/store/pay?orderid={id}
```

5. Start the server:

```bash
uvicorn base:app --host 0.0.0.0 --port 8000
```

> Make sure your `BASE_URL` is publicly accessible (e.g. via a domain or ngrok) so RupantorPay can reach the webhook.

---

If you find this project useful, please consider ⭐ starring the repository!
