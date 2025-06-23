import random
import json
from locust import HttpUser, task, between, events

# Add this for debugging
@events.request.add_listener
def print_request_info(request_type, name, response_time, response_length, exception, **kwargs):
    print(f"Request: {request_type} {name}, Response time: {response_time}ms, Exception: {exception}")

class UserAPIUser(HttpUser):
    wait_time = between(1, 3)
    users_cache = []
    groups_cache = []
    
    def on_start(self):
        print("User started - fetching all users")
        self.fetch_all_users()
    
    def fetch_all_users(self):
        print("Attempting to fetch all users...")
        try:
            with self.client.get("/api/user/all", catch_response=True, name="Get All Users") as response:
                print(f"Status: {response.status_code}, Response length: {len(response.text)}")
                if response.status_code == 200:
                    users = response.json()
                    self.users_cache = users
                    print(f"Cached {len(users)} users")
                    self.extract_groups()
                    response.success()
                else:
                    print(f"Failed with status {response.status_code}: {response.text}")
                    response.failure(f"Failed with status {response.status_code}")
        except Exception as e:
            print(f"Exception in fetch_all_users: {e}")
    
    def extract_groups(self):
        groups = set()
        for user in self.users_cache:
            if 'groups' in user and user['groups']:
                for group in user['groups']:
                    groups.add(group)
        self.groups_cache = list(groups)
        print(f"Extracted {len(self.groups_cache)} groups: {self.groups_cache}")
    
    @task(3)
    def get_all_users(self):
        print("Task: get_all_users")
        self.client.get("/api/user/all", name="Get All Users")
    
    @task(5)
    def get_user_by_id(self):
        print("Task: get_user_by_id")
        if not self.users_cache:
            self.fetch_all_users()
            return
            
        user = random.choice(self.users_cache)
        if 'id' in user:
            user_id = user['id']
            print(f"Getting user by ID: {user_id}")
            self.client.get(f"/api/user/id/{user_id}", name="Get User by ID")
    
    @task(5)
    def get_user_by_username(self):
        print("Task: get_user_by_username")
        if not self.users_cache:
            self.fetch_all_users()
            return
            
        user = random.choice(self.users_cache)
        if 'username' in user:
            username = user['username']
            print(f"Getting user by username: {username}")
            self.client.get(f"/api/user/username/{username}", name="Get User by Username")
    
    @task(2)
    def get_users_by_group(self):
        print("Task: get_users_by_group")
        if not self.groups_cache:
            if not self.users_cache:
                self.fetch_all_users()
                return
            self.extract_groups()
            
        if self.groups_cache:
            group = random.choice(self.groups_cache)
            print(f"Getting users by group: {group}")
            self.client.get(f"/api/user/group/{group}", name="Get Users by Group")