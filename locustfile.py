import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000/"
    #host = "https://alex-online-store.fly.dev/"

    @task
    def hello_world(self):
        self.client.get("api/v1/shop/guest_user/get_all_categories")
        self.client.get("api/v1/shop/guest_user/search")
        self.client.get("api/v1/shop/guest_user/store_info")
        self.client.get("api/v1/shop/guest_user/banner_list")

    #
    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/api/v1/shop/guest_user/product/{item_id}", name="/item")
    #         time.sleep(1)
    #
    # def on_start(self):
    #     self.client.post("/api/v1/shop/auth_user/test/", json={"username":"foo", "password":"bar"})
