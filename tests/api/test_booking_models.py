
import pytest
from pydantic import ValidationError

from models.booking_model import Bookingrequest


@pytest.mark.api
def test_valid_booking_model():

    payload = {
        "firstname": "Akash",
        "lastname": "Joshi",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05"
        }
    }

    booking = Bookingrequest.model_validate(payload)

    assert booking.firstname == "Akash"
    assert booking.totalprice == 1500


@pytest.mark.api
def test_invalid_booking_price():

    payload = {
        "firstname": "Akash",
        "lastname": "Joshi",
        "totalprice": "invalid",
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05"
        }
    }

    with pytest.raises(ValidationError):
        Bookingrequest.model_validate(payload)


@pytest.mark.api
def test_invalid_booking_dates():

    payload = {
        "firstname": "Akash",
        "lastname": "Joshi",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-05",
            "checkout": "2026-12-01"
        }
    }

    with pytest.raises(ValidationError):
        Bookingrequest.model_validate(payload)


@pytest.mark.api
def test_missing_required_field():

    payload = {
        "firstname": "Akash",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05"
        }
    }

    with pytest.raises(ValidationError):
        Bookingrequest.model_validate(payload)
