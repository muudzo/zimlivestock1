import os
from fastapi.testclient import TestClient
from app.main import app
from app.database import create_db_and_tables, get_session
from app.services import _get_paynow, initiate_web_payment, initiate_mobile_payment, check_payment_status
from sqlmodel import delete
import pytest

client = TestClient(app)


def setup_module(module):
    # ensure fresh database for tests
    create_db_and_tables()


@pytest.fixture(autouse=True)
def reset_db():
    # clear tables before each test so the state is predictable
    from app.models import User, LivestockItem, Payment
    with next(get_session()) as session:
        session.exec(delete(User))
        session.exec(delete(LivestockItem))
        session.exec(delete(Payment))
        session.commit()
    yield


class DummyUser:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@pytest.fixture(autouse=True)
def cleanup_db():
    # for a real test suite you'd drop tables or use a temporary file
    yield


def test_register_and_login():
    # register new user
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "phone": "0777000000",
        "password": "secret"
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200, r.text
    user = r.json()
    assert user["email"] == payload["email"]
    assert str(user["id"]).isdigit()

    # duplicate registration by email
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400
    assert "Email already registered" in r2.text

    # login with email
    r3 = client.post("/auth/login", json={"contact": payload["email"], "password": "secret"})
    assert r3.status_code == 200
    token_data = r3.json()
    assert "access_token" in token_data

    # login with phone
    r4 = client.post("/auth/login", json={"contact": payload["phone"], "password": "secret"})
    assert r4.status_code == 200

    # wrong password
    r5 = client.post("/auth/login", json={"contact": payload["email"], "password": "wrong"})
    assert r5.status_code == 401


def test_paynow_env_and_service(monkeypatch):
    # monkeypatch environment to simulate missing credentials
    monkeypatch.delenv("PAYNOW_INTEGRATION_ID", raising=False)
    monkeypatch.delenv("PAYNOW_INTEGRATION_KEY", raising=False)
    with pytest.raises(EnvironmentError):
        _get_paynow()

    # set bogus credentials and ensure we can create instance but remote calls fail
    monkeypatch.setenv("PAYNOW_INTEGRATION_ID", "id123")
    monkeypatch.setenv("PAYNOW_INTEGRATION_KEY", "key123")
    paynow = _get_paynow()
    assert paynow is not None

    # attempting to initiate payments without valid credentials will raise later
    with pytest.raises(Exception):
        initiate_web_payment("ref123", "test@test.com", "descr", 10.0)

    # mobile with invalid method
    with pytest.raises(ValueError):
        initiate_mobile_payment("ref", "a@b.com", "descr", 5.0, "0777000000", "invalid")


def test_payments_endpoints_validation():
    # missing livestock should return 404
    r = client.post("/payments/initiate", json={
        "livestock_id": 999,
        "bid_id": 1,
        "payer_id": 1,
        "payment_method": "web"
    })
    assert r.status_code == 404

    # create a dummy user and dummy item to satisfy validation
    # we can call directly on database if needed
    from app.database import get_session
    from app.models import User, LivestockItem
    from datetime import datetime

    with next(get_session()) as session:
        u = User(firstName="A", lastName="B", email="a@b.com", phone="0777000001", password_hash="xxx")
        session.add(u)
        session.commit()
        session.refresh(u)
        item = LivestockItem(
            title="foo",
            breed="bar",
            age="1",
            weight="10",
            location="here",
            startingPrice=100,
            category="cattle",
            imageUrl="",
            auctionEndDate=datetime(2024, 1, 1),
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        # now initiate
        r2 = client.post("/payments/initiate", json={
            "livestock_id": item.id,
            "bid_id": 0,
            "payer_id": u.id,
            "payment_method": "web"
        })
        # should be pending (200) or paynow creds invalid (400) or service unavailable (503)
        assert r2.status_code in (200, 400, 503)
