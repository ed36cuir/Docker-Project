import random
from locust import HttpLocust, task, between

class WebsiteUser(HttpLocust):
    wait_time = between(5, 9)

    @task(2)
    def index(self):
        self.client.get("/")
        self.client.get("/ajax-notifications/")

    @task(1)
    def view_post(self):
        post_id = random.randint(1, 10000)
        self.client.get("/post?id=%i" % post_id, name="/post?id=[post-id]")

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        self.client.post("/login", {"username":"ellen_key", "password":"education"})