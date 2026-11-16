from api_clients.base_api_client import BaseApiClient


class BookingAPI(BaseApiClient):
    def authenticate(self, username, password):

        payload = {
            "username": username,
            "password": password
        }

        return self.request(
            "POST",
            "/auth",
            json=payload
        )

    def set_auth_token(self, token):

        self.session.headers.update({
            "Cookie": f"token={token}"
        })

    def get_bookings(self):

        return self.request(
            "GET",
            "/booking"
        )

    def get_booking(self, booking_id):

        return self.request(
            "GET",
            f"/booking/{booking_id}"
        )

    def create_booking(self, payload):

        return self.request(
            "POST",
            "/booking",
            json=payload
        )

    def update_booking(self, booking_id, payload):

        return self.request(
            "PUT",
            f"/booking/{booking_id}",
            json=payload
        )

    def partial_update_booking(
        self,
        booking_id,
        payload
    ):

        return self.request(
            "PATCH",
            f"/booking/{booking_id}",
            json=payload
        )

    def delete_booking(self, booking_id):

        return self.request(
            "DELETE",
            f"/booking/{booking_id}"
        )
