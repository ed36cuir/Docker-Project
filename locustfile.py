from locust import HttpLocust, TaskSet, betweem

def index(l):
    l.client.get("/")
    
class UserBehavior(TaskSet):
    task = {index:1}
    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = betweem(5.0, 9.0)