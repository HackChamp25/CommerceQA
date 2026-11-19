"""Fixed UI paths and API endpoints. Prefer these over hardcoded strings."""


class UIPaths:
    LOGIN = "/"
    INVENTORY = "/inventory.html"
    CART = "/cart.html"


class ApiEndpoints:
    AUTH = "/auth"
    BOOKINGS = "/booking"

    @staticmethod
    def booking(booking_id: int | str) -> str:
        return f"/booking/{booking_id}"


# Version-specific base URLs (extend when v2 screens/APIs differ)
VERSION_URLS = {
    "v1": {
        "ui_base_url": "https://www.saucedemo.com",
        "api_base_url": "https://restful-booker.herokuapp.com",
    },
    "v2": {
        # Placeholder until a real v2 app exists
        "ui_base_url": "https://www.saucedemo.com",
        "api_base_url": "https://restful-booker.herokuapp.com",
    },
}
