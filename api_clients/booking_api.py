from api_clients.base_api_client import BaseApiClient
from config.constants import Headers, Payloads
from config.endpoints import ApiEndpoints


class BookingAPI(BaseApiClient):
    def authenticate(self, username, password):
        return self.request(
            "POST",
            ApiEndpoints.AUTH,
            json=Payloads.auth(username, password),
        )

    def set_auth_token(self, token):
        self.session.headers.update(Headers.token_cookie(token))

    def get_bookings(self):
        return self.request("GET", ApiEndpoints.BOOKINGS)

    def get_booking(self, booking_id):
        return self.request("GET", ApiEndpoints.booking(booking_id))

    def create_booking(self, payload):
        return self.request("POST", ApiEndpoints.BOOKINGS, json=payload)

    def update_booking(self, booking_id, payload):
        return self.request(
            "PUT",
            ApiEndpoints.booking(booking_id),
            json=payload,
        )

    def partial_update_booking(self, booking_id, payload):
        return self.request(
            "PATCH",
            ApiEndpoints.booking(booking_id),
            json=payload,
        )

    def delete_booking(self, booking_id):
        return self.request("DELETE", ApiEndpoints.booking(booking_id))
