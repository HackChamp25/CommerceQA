import allure
import pytest

from models.booking_model import (
    BookingCreateresponse,
    Bookingrequest,
    Bookingresponse,
)
from utils.allure_helpers import attach_api_response
from utils.test_data_reader import load_test_data


@allure.epic("CommerceQA")
@allure.feature("Booking API")
@allure.story("Create Booking")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify successful booking creation")
@allure.description(
    "Verify that a booking can be created successfully."
)
@pytest.mark.api
@pytest.mark.smoke
def test_create_booking(booking_api):
    raw_data = load_test_data("booking_data.json")
    request_model = Bookingrequest.model_validate(raw_data)
    with allure.step("Create booking"):
        response = booking_api.create_booking(request_model.model_dump(mode="json"))
    with allure.step("Verify booking creation"):
        assert response.status_code == 200
        response_model = BookingCreateresponse.model_validate_json(response.text)
        assert response_model.bookingid > 0
        assert response_model.booking.firstname == request_model.firstname
        assert response_model.booking.totalprice == request_model.totalprice
    attach_api_response(response)
    assert response.status_code == 200
    response_model = BookingCreateresponse.model_validate_json(response.text)
    assert response_model.bookingid > 0
    assert response_model.booking.firstname == request_model.firstname
    assert response_model.booking.totalprice == request_model.totalprice

def test_get_booking_by_id(booking_api):
    raw_data = load_test_data("booking_data.json")
    request_model = Bookingrequest.model_validate(raw_data)
    response = booking_api.create_booking(request_model.model_dump(mode="json"))
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    response = booking_api.get_booking(booking_id)
    assert response.status_code == 200
    response_model = Bookingresponse.model_validate_json(response.text)
    assert response_model.firstname == request_model.firstname
    assert response_model.totalprice == request_model.totalprice


@pytest.mark.api
@pytest.mark.regression
def test_update_booking(authenticated_booking_api):
    raw_data = load_test_data("booking_data.json")
    create_model = Bookingrequest.model_validate(raw_data)
    create_response = authenticated_booking_api.create_booking(
        create_model.model_dump(mode="json")
    )
    assert create_response.status_code == 200
    booking_id = create_response.json()["bookingid"]

    update_payload = create_model.model_dump(mode="json")
    update_payload["firstname"] = "Updated"
    update_payload["totalprice"] = 2500
    update_model = Bookingrequest.model_validate(update_payload)

    update_response = authenticated_booking_api.update_booking(
        booking_id,
        update_model.model_dump(mode="json"),
    )
    assert update_response.status_code == 200
    response_model = Bookingresponse.model_validate_json(update_response.text)
    assert response_model.firstname == "Updated"
    assert response_model.totalprice == 2500

