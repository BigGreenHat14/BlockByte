import pickle
import os
import scratchattach as sa
import threading

# Global storage for projects
projects = {}

# Utility functions for persistent data storage
def save_data(project_id, userbytoken, users):
    with open(f"blockbytedb_{project_id}", "wb") as f:
        pickle.dump((userbytoken, users), f)

def load_data(project_id):
    if os.path.exists(f"blockbytedb_{project_id}"):
        with open(f"blockbytedb_{project_id}", "rb") as f:
            return pickle.load(f)
    else:
        return ({}, {})

# User class
class User:
    def __init__(self, uuid, name):
        self.uuid = uuid
        self.name = name
        self.theme = "56.7"
        self.balance = 100.0
        self.notifications = []

    def get_balance(self):
        return round(self.balance)

    def transfer(self, amount, recipient):
        if amount > self.balance or amount < 1:
            return "x"
        self.balance -= amount
        recipient.balance += amount
        recipient.notifications.append(f"{self.name} sent you {amount} BlockByte{'' if amount == 1 else 's'}!")
        return "k"

# Generate UUID
def get_uuid():
    import uuid
    return str(uuid.uuid4())

# Project initialization
def init_project(project_id):
    cloud = session.get_tw_cloud(project_id)
    client = cloud.requests()

    userbytoken, users = load_data(project_id)

    @client.request
    def login(token):
        try:
            return list(users.keys())[list(users.values()).index(token)]
        except:
            return "x"

    @client.request
    def signup(username):
        if username in list(users.keys()):
            return "x"
        uuid = get_uuid()
        users[username] = uuid
        userbytoken[uuid] = User(uuid, username)
        save_data(project_id, userbytoken, users)
        return uuid

    @client.request
    def info(token):
        try:
            user = userbytoken[token]
            return [user.balance, user.theme] + list(reversed(user.notifications))
        except Exception as e:
            return ["Invalid Token", "0", str(type(e)), str(e)]

    @client.request
    def dismiss(token):
        userbytoken[token].notifications = []
        save_data(project_id, userbytoken, users)
        return "k"

    @client.request
    def transfer(token, othername, amount):
        try:
            user = userbytoken[token]
            user2 = userbytoken[users[othername]]
            return user.transfer(int(amount), user2)
        except:
            return "x"

    @client.request
    def leaderboard():
        try:
            sorted_users = sorted(userbytoken.values(), key=lambda u: u.balance, reverse=True)
            return [f"{user.name}: {user.get_balance()}" for user in sorted_users]
        except Exception as e:
            return [str(type(e)), str(e)]

    @client.request
    def get_balance(othername):
        try:
            user = userbytoken[users[othername]]
            return str(user.get_balance())
        except:
            return "x"

    @client.request
    def set_theme(token, theme):
        try:
            userbytoken[token].theme = theme
            save_data(project_id, userbytoken, users)
            return "k"
        except:
            return "x"

    @client.event
    def on_ready():
        print(f"Server for project {project_id} is running :D")

    client.start(thread=True)
    return client

# Add projects
def add_project(project_id):
    if project_id not in projects:
        projects[project_id] = init_project(project_id)
    else:
        print(f"Project {project_id} is already initialized.")

############
# Settings #
############
PROJECT_IDS = [1116465685, 1116273299]

# Start projects
for project_id in PROJECT_IDS:
    threading.Thread(target=add_project, args=(project_id,)).start()

while True:
    pass
