import random

from locust import HttpUser, task, between, events


class BookingUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Authenticate when each simulated user starts."""
        response = self.client.post(
            "/auth",
            json={
                "username": "admin",
                "password": "password123"
            },
            name="POST /auth"
        )

        if response.status_code == 200:
            self.token = response.json()["token"]
            self.headers = {"Cookie": f"token={self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(3)
    def get_booking_ids(self):
        self.client.get(
            "/booking",
            name="GET /booking"
        )

    @task(1)
    def get_booking_details(self):
        response = self.client.get(
            "/booking",
            name="GET /booking"
        )

        if response.status_code == 200:
            bookings = response.json()

            if bookings:
                booking_id = random.choice(bookings)["bookingid"]

                self.client.get(
                    f"/booking/{booking_id}",
                    name="GET /booking/[id]"
                )
    
    @events.quitting.add_listener
    def check_performance_thresholds(environment, **kwargs):
        stats = environment.stats.total
    
        if stats.num_requests == 0:
            print("No requests were recorded.")
            environment.process_exit_code = 1
            return
    
        failure_rate = stats.fail_ratio * 100
        p95 = stats.get_response_time_percentile(0.95)
    
        print("\n========== PERFORMANCE CHECK ==========")
        print(f"Failure rate: {failure_rate:.2f}%")
        print(f"P95 response time: {p95:.2f} ms")
    
        failed = False
    
        if failure_rate > 1:
            print("FAIL: Failure rate exceeded 1%.")
            failed = True
    
        if p95 > 1500:
            print("FAIL: P95 response time exceeded 1500 ms.")
            failed = True
    
        if failed:
            environment.process_exit_code = 1
            print("PERFORMANCE TEST: FAILED")
        else:
            environment.process_exit_code = 0
            print("PERFORMANCE TEST: PASSED")