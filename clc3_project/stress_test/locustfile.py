import random
from locust import HttpUser, task, between


class ConcertUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)
    active_concert_ids = []

    @task(3)
    def browse_concerts(self):
        """Fetches the list of IDs from your endpoint"""
        with self.client.get("/concerts", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                self.active_concert_ids = [item["id"] for item in data]
            else:
                response.failure(f"Failed to fetch concerts: {response.status_code}")

    @task(1)
    def buy_ticket(self):
        """Attempts to buy a random concert using an email address"""
        if not self.active_concert_ids:
            return

        concert_id = random.choice(self.active_concert_ids)

        # Generating a dynamic email to simulate different customers
        random_suffix = random.randint(1, 10000)
        random_quantity = random.randint(1, 5)
        payload = {
            "user_email": f"testuser_{random_suffix}@example.com",
            "quantity": random_quantity,
        }

        # Use the name parameter to keep your Grafana dashboard clean
        self.client.post(f"/buy_random_deny/{concert_id}", json=payload, name="/buy_random_deny/[id]")