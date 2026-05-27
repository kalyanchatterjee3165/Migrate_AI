"""
Schema profiles — each is a dict mapping column_name → callable that returns a value.
data_factory.py uses these to build DataFrames.
"""

from .base_generator import (
    fake_id, fake_name, fake_email, fake_phone, fake_address,
    fake_company, fake_date, fake_datetime, fake_amount,
    fake_status, fake_uuid, fake_url, fake_country, fake_city,
)


def users_profile(i: int) -> dict:
    return {
        "id":         fake_id(i),
        "uuid":       fake_uuid(),
        "name":       fake_name(),
        "email":      fake_email(),
        "phone":      fake_phone(),
        "address":    fake_address(),
        "city":       fake_city(),
        "country":    fake_country(),
        "created_at": fake_datetime(),
        "status":     fake_status(["active", "inactive", "pending"]),
    }


def orders_profile(i: int) -> dict:
    return {
        "order_id":   fake_id(i),
        "user_id":    fake_id(i % 50),        # simulate FK to ~50 users
        "product":    fake_company() + " Item",
        "quantity":   fake_id(i % 10),
        "unit_price": fake_amount(),
        "total":      fake_amount(),
        "status":     fake_status(["placed", "shipped", "delivered", "cancelled"]),
        "order_date": fake_date(),
        "shipped_at": fake_datetime(),
    }


def events_profile(i: int) -> dict:
    return {
        "event_id":   fake_uuid(),
        "user_id":    fake_id(i % 50),
        "event_type": fake_status(["click", "view", "purchase", "signup", "logout"]),
        "page":       fake_url(),
        "session_id": fake_uuid(),
        "timestamp":  fake_datetime(),
        "country":    fake_country(),
        "device":     fake_status(["mobile", "desktop", "tablet"]),
    }


def products_profile(i: int) -> dict:
    return {
        "product_id": fake_id(i),
        "sku":        fake_uuid()[:8].upper(),
        "name":       fake_company() + " Pro",
        "category":   fake_status(["electronics", "clothing", "food", "tools", "books"]),
        "price":      fake_amount(),
        "stock":      fake_id(i % 500),
        "created_at": fake_date(),
        "active":     fake_status([True, False]),
    }


def transactions_profile(i: int) -> dict:
    return {
        "txn_id":       fake_uuid(),
        "account_id":   fake_id(i % 100),
        "type":         fake_status(["credit", "debit"]),
        "amount":       fake_amount(),
        "currency":     fake_status(["USD", "EUR", "GBP", "INR"]),
        "status":       fake_status(["completed", "pending", "failed"]),
        "created_at":   fake_datetime(),
        "reference":    fake_uuid()[:12].upper(),
    }


# Registry of all available profiles
PROFILES = {
    "users":        users_profile,
    "orders":       orders_profile,
    "events":       events_profile,
    "products":     products_profile,
    "transactions": transactions_profile,
}

DEFAULT_PROFILE = "users"