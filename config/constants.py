"""Fixed credentials, payloads, headers, and status values used across the framework."""


class Users:
    STANDARD = {"username": "standard_user", "password": "secret_sauce"}
    LOCKED = {"username": "locked_out_user", "password": "secret_sauce"}
    INVALID = {"username": "invalid_user", "password": "wrong_password"}


class ApiAuth:
    ADMIN = {"username": "admin", "password": "password123"}


class Headers:
    JSON = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    @staticmethod
    def token_cookie(token: str) -> dict:
        return {"Cookie": f"token={token}"}


class StatusCode:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405


class Payloads:
    """Reusable payload templates (tests may still load JSON for richer data)."""

    DEFAULT_BOOKING = {
        "firstname": "Akash",
        "lastname": "Joshi",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05",
        },
        "additionalneeds": "Breakfast",
    }

    @staticmethod
    def auth(username: str, password: str) -> dict:
        return {"username": username, "password": password}
