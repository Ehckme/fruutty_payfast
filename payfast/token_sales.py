# payfast/token_sales.py
import os, uuid
from config import Config
import datetime
import traceback
from sqlalchemy import select
from random import choices
import string
import random
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from authentication.database.extensions import db # replace with your actual app import
from authentication.database.model import Users, Fruutty_token, PayFastUsers, TokenPurchase, QRToken
from payfast.utils import (
    generate_signature, PROCESS_URL, PAYFAST_PASSPHRASE,
    make_token_code, generate_qr, validate_payfast_with_server, send_receipt_email
)
from urllib.parse import urlencode


QR_SAVE_DIR = os.getenv("QR_CODES_DIR", "static/qr_codes")

# Original bundles
BUNDLES = [10, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000]
# ----- Buy route -----

payfast_bp = Blueprint("payfast_bp", __name__, template_folder="templates")



#---------------------------------------------------------------------



@payfast_bp.route("/buy", methods=["GET"])
@login_required
def buy_default():
    return render_template("choose_bundle.html", bundles=BUNDLES)


# --- helper inside token_sales.py ---
def random_chars(length):
    import string, random
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# --- BUY ROUTE ---
@payfast_bp.route("/buy/<bundle>", methods=["GET"])
@login_required
def buy(bundle):
    bundle_prices = {
        "10": 10.00, "50": 50.00, "100": 100.00, "200": 200.00,
        "300": 300.00, "500": 500.00, "1000": 1000.00, "2000": 2000.00,
        "3000": 3000.00, "5000": 5000.00
    }

    if bundle not in bundle_prices:
        return "Invalid bundle", 400

    # Create TokenPurchase row first
    purchase = TokenPurchase(
        user_email=current_user.email,
        user_id=current_user.id,
        bundle_id=int(bundle),
        amount=bundle_prices[bundle],
        status="pending"
    )
    db.session.add(purchase)
    db.session.commit()  # to get purchase.id

    pfData = {
        "merchant_id": os.getenv("PAYFAST_MERCHANT_ID"),
        "merchant_key": os.getenv("PAYFAST_MERCHANT_KEY"),
        "return_url": os.getenv("PAYFAST_RETURN_URL"),
        "cancel_url": os.getenv("PAYFAST_CANCEL_URL"),
        "notify_url": os.getenv("PAYFAST_NOTIFY_URL"),
        "m_payment_id": str(uuid.uuid4()),
        "amount": f"{bundle_prices[bundle]:.2f}",
        "item_name": f"Token Bundle {bundle}",
        "custom_str1": str(purchase.id),
        "custom_str2": current_user.email
    }

    pfData["signature"] = generate_signature(pfData, os.getenv("PAYFAST_PASSPHRASE", ""))

    return render_template("payfast_form.html", pfData=pfData)


# --- NOTIFY ROUTE ---
import requests 

@payfast_bp.route("/notify", methods=["POST"])
def notify():
    try:
        data = request.form.to_dict()
        current_app.logger.info(f"PAYFAST NOTIFY RECEIVED: {data}")

        if not validate_payfast_with_server(data):
            current_app.logger.warning("PAYFAST VALIDATION FAILED.")
            return "Invalid", 400

        purchase_id = data.get("custom_str1")
        if not purchase_id:
            current_app.logger.error("No purchase ID in notify payload.")
            return "Missing purchase_id", 400

        purchase = TokenPurchase.query.get(purchase_id)
        if not purchase:
            current_app.logger.error(f"No purchase found with id={purchase_id}")
            return "No purchase", 400

        user = Users.query.filter_by(email=purchase.user_email).first()
        if not user:
            current_app.logger.error(f"No user found for email={purchase.user_email}")
            return "No user", 400

        amount_paid = float(data.get("amount_gross", 0))
        if amount_paid <= 0:
            current_app.logger.warning(f"Zero or missing amount: {data}")
            return "Invalid amount", 400

        # Complete purchase
        purchase.status = "completed"
        purchase.payfast_ref = data.get("pf_payment_id")
        purchase.amount = amount_paid

        # CREDIT USER TOKENS
        tokens_bought = amount_paid
        user.fruutty_token = (user.fruutty_token or 0) + tokens_bought

        # CUMULATIVE SOLD TOKENS
        sold_tokens_sum = db.session.query(db.func.sum(Fruutty_token.sold_tokens)).scalar() or 0
        sold_token_to_db = sold_tokens_sum + tokens_bought
        available_tokens_to_db = float(Config.BASE_TOKEN) - sold_token_to_db

        # Use last row for opening/closing trades
        last_ft = Fruutty_token.query.order_by(Fruutty_token.date.desc()).first()
        opening_trade = float(last_ft.opening_trade) if last_ft else 0
        closing_trade = float(last_ft.closing_trade) if last_ft else 0

        # Generate new token_id
        four_digits = random_chars(4)
        two_digits = random_chars(2)
        token_id = f"{Config.TOKEN_ID}{four_digits}_{two_digits}"

        # Create new Fruutty_token row
        new_ft = Fruutty_token(
            token_id=token_id,
            initial_base_token=float(Config.BASE_TOKEN),
            available_tokens=available_tokens_to_db,
            sold_tokens=sold_token_to_db,
            opening_trade=opening_trade,
            closing_trade=closing_trade,
        )

        db.session.add(new_ft)
        db.session.commit()

        current_app.logger.info(
            f"PAYFAST SUCCESS: User {user.email} credited {tokens_bought} tokens. "
            f"Available tokens now: {available_tokens_to_db}"
        )
        return "OK", 200

    except Exception:
        current_app.logger.exception("Error in PayFast notify:")
        db.session.rollback()
        return "Error", 500








# ----- Success -----

@payfast_bp.route("/return", methods=["GET", "POST"])
def payfast_return():
    # User is redirected here after successful payment
    return render_template("payfast_return.html")






@payfast_bp.route("/cancel", methods=["GET", "POST"])
def payfast_cancel():
    # User is redirected here if they cancel at PayFast
    return render_template("payfast_cancel.html")

