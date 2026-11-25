"""Verify server-recorded purchases with a mocked gateway and an in-memory ledger."""

import ast
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from types import SimpleNamespace
import uuid

from flask import Flask, request, jsonify
import pytest

from services.gateway_orders import create_gateway_order_schema


@pytest.fixture
def checkout():
    database = sqlite3.connect(":memory:")
    database.row_factory = sqlite3.Row
    database.executescript("""
        CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, email TEXT);
        INSERT INTO intern_accounts VALUES (1, 'learner@example.test');
        CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, price_inr INTEGER);
        INSERT INTO courses VALUES (7, 'Sample course', 600);
        CREATE TABLE applications (id INTEGER PRIMARY KEY, email TEXT);
        CREATE TABLE course_payments (
            id INTEGER PRIMARY KEY, intern_id INTEGER, course_id INTEGER, course_title TEXT,
            amount INTEGER, created_at TEXT, payment_screenshot TEXT, status TEXT,
            admin_note TEXT, updated_at TEXT, razorpay_order_id TEXT, razorpay_payment_id TEXT,
            razorpay_signature TEXT
        );
        CREATE TABLE payment_events (
            id INTEGER PRIMARY KEY, event_id TEXT UNIQUE, event_type TEXT, payload TEXT, status TEXT
        );
    """)
    create_gateway_order_schema(database)
    app = Flask(__name__)
    user = {"id": 1, "email": "learner@example.test"}
    capture = {"id": "pay_demo", "order_id": "order_demo", "amount": 60000, "currency": "INR", "status": "captured"}
    fetched = []

    def fetch_payment(payment_id):
        fetched.append(payment_id)
        return capture

    gateway = SimpleNamespace(
        RazorpayError=RuntimeError,
        is_razorpay_enabled=lambda: True,
        create_order=lambda amount_inr, **options: {
            "order_id": "order_demo", "amount": amount_inr * 100, "currency": "INR", "key_id": "test-key",
        },
        verify_payment_signature=lambda *args: True,
        get_razorpay_keys=lambda: ("", "", "test-webhook"),
        verify_webhook_signature=lambda body, signature: signature == "test-webhook-signature",
        fetch_payment=fetch_payment,
    )
    namespaces = {
        "app": app, "request": request, "jsonify": jsonify, "re": re, "datetime": datetime, "uuid": uuid,
        "get_db": lambda: database, "require_role": lambda role: user,
        "clean_text": lambda value: value.strip() if isinstance(value, str) else "",
        "normalize_domain_string": lambda value: value,
        "now_str": lambda: "2026-01-01 01:02:03",
        "log_error": lambda *args: None, "razorpay_client": gateway,
        "hashlib": hashlib, "json": json,
    }
    source_path = Path(__file__).resolve().parents[1] / "app.py"
    parsed = ast.parse(source_path.read_text(encoding="utf-8-sig"))
    names = {
        "api_razorpay_create_order", "api_razorpay_verify_payment", "api_razorpay_webhook",
        "_gateway_payment_result", "_fulfill_gateway_capture", "_notify_gateway_enrollment",
    }
    routes = [node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name in names]
    exec(compile(ast.Module(body=routes, type_ignores=[]), str(source_path), "exec"), namespaces)
    client = app.test_client()
    created = client.post("/api/payment/razorpay/create-order", json={"product_type": "course", "product_id": 7})
    assert created.status_code == 200
    assert created.json["amount"] == 60000
    try:
        yield client, database, user, capture, fetched
    finally:
        database.close()


def verify(client):
    return client.post("/api/payment/razorpay/verify-payment", json={
        "razorpay_order_id": "order_demo",
        "razorpay_payment_id": "pay_demo",
        "razorpay_signature": "test-signature",
    })


def webhook(client, capture, signature="test-webhook-signature"):
    return client.post("/api/payment/razorpay/webhook", json={
        "event": "payment.captured",
        "payload": {"payment": {"entity": capture}},
    }, headers={
        "X-Razorpay-Event-Id": "event-test",
        "X-Razorpay-Signature": signature,
    })


@pytest.mark.parametrize("field,value", [("amount", 500), ("currency", "USD"), ("status", "authorized")])
def test_nonmatching_capture_does_not_credit(checkout, field, value):
    client, database, _, capture, _ = checkout
    capture[field] = value
    assert verify(client).status_code == 409
    assert database.execute("SELECT payment_id FROM gateway_payment_orders").fetchone()[0] is None
    assert database.execute("SELECT COUNT(*) FROM course_payments").fetchone()[0] == 0


def test_payment_is_bound_to_buyer_and_saved_purchase(checkout):
    client, database, user, _, fetched = checkout
    user["id"] = 2
    assert verify(client).status_code == 404
    assert fetched == []
    user["id"] = 1
    database.execute("UPDATE courses SET price_inr=999 WHERE id=7")
    response = verify(client)
    assert response.status_code == 200
    assert response.json["redirect"] == "/courses/7"
    assert verify(client).status_code == 200
    assert fetched == ["pay_demo"]
    assert tuple(database.execute(
        "SELECT intern_id, course_id, amount, status FROM course_payments"
    ).fetchone()) == (1, 7, 600, "verified")


def test_signed_webhook_and_checkout_share_one_credit(checkout):
    client, database, _, capture, fetched = checkout
    assert webhook(client, capture).status_code == 200
    repeated = webhook(client, capture)
    assert "Duplicate" in repeated.json["message"]
    assert verify(client).status_code == 200
    assert fetched == []
    assert database.execute("SELECT COUNT(*) FROM course_payments").fetchone()[0] == 1
    assert database.execute("SELECT status FROM payment_events").fetchone()[0] == "processed"


def test_webhook_requires_signature_and_logs_unmatched_reference(checkout):
    client, database, _, capture, _ = checkout
    assert webhook(client, capture, signature="other").status_code == 400
    assert database.execute("SELECT COUNT(*) FROM payment_events").fetchone()[0] == 0
    capture["amount"] = 1
    capture["email"] = "sample@example.test"
    assert webhook(client, capture).status_code == 200
    event = database.execute("SELECT status, payload FROM payment_events").fetchone()
    assert event["status"] == "unmatched"
    assert "sample@example.test" not in event["payload"]
    assert database.execute("SELECT COUNT(*) FROM course_payments").fetchone()[0] == 0
