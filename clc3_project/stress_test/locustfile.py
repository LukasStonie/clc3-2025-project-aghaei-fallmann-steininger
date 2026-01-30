from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(2, 5)

    @task
    def hello_world(self):
        self.client.post("/buy/123", json={"user_id": "user_1", "quantity": 2})
