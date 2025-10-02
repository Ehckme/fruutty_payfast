# payfast/utils.py
import os, uuid, hashlib, urllib.parse, smtplib
from hashlib import md5
from qrcode import make as qrcode_make
from email.message import EmailMessage

# Env config
PAYFAST_MERCHANT_ID = os.getenv("PAYFAST_MERCHANT_ID")
PAYFAST_MERCHANT_KEY = os.getenv("PAYFAST_MERCHANT_KEY")
PAYFAST_PASSPHRASE = os.getenv("PAYFAST_PASSPHRASE", "")
PAYFAST_SANDBOX = os.getenv("PAYFAST_SANDBOX", "1") == "1"

PROCESS_URL = "https://sandbox.payfast.co.za/eng/process?" if PAYFAST_SANDBOX else "https://www.payfast.co.za/eng/process?"
VALIDATE_URL = "https://sandbox.payfast.co.za/eng/query/validate" if PAYFAST_SANDBOX else "https://www.payfast.co.za/eng/query/validate"

def make_token_code():
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()[:20]

def generate_qr(data_str: str, save_dir: str, filename: str):
    os.makedirs(save_dir, exist_ok=True)
    img = qrcode_make(data_str)
    path = os.path.join(save_dir, filename)
    img.save(path)
    return path


def generate_signature(data: dict, passphrase: str = "") -> str:
    """
    Generate a PayFast signature in the order fields are added.
    """
    payload = ""
    for key in data:
        value = str(data[key])
        payload += f"{key}={urllib.parse.quote_plus(value.replace('+', ' '))}&"

    payload = payload[:-1]  # strip trailing &
    if passphrase:
        payload += f"&passphrase={passphrase}"

    return hashlib.md5(payload.encode()).hexdigest()




def validate_payfast_with_server(payload: dict) -> bool:
    import requests
    r = requests.post(VALIDATE_URL, data=payload, timeout=10)
    return r.ok and r.text.strip().upper().startswith("VALID")

def send_receipt_email(smtp_config: dict, to_email: str, subject: str, body: str, attachment_path: str = None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_config["from_email"]
    msg["To"] = to_email
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            data = f.read()
        import imghdr
        img_type = imghdr.what(None, data)
        msg.add_attachment(data, maintype="image", subtype=img_type, filename=os.path.basename(attachment_path))

    with smtplib.SMTP(smtp_config["host"], smtp_config.get("port", 25)) as s:
        if smtp_config.get("starttls"):
            s.starttls()
        if smtp_config.get("username"):
            s.login(smtp_config["username"], smtp_config["password"])
        s.send_message(msg)

