############
# Settings #
############
USERNAME = ""
PASSWORD = ""
############
import pickle
import os
import scratchattach as sa
import requests
import bghsecrets
import math

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
    session = sa.login(USERNAME, PASSWORD)
    cloud = session.connect_tw_cloud(project_id, contact="@BigGreenHat on Scratch")
    client = cloud.requests()

    userbytoken, users = load_data(project_id)

    # Register project-specific client event handlers
    @client.request
    def login(token):
        try:
            return list(users.keys())[list(users.values()).index(token)]
        except:
            return "x"

    @client.request
    def signup(username):
        print(users)
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
            toreturn = []
            user = userbytoken[token]
            toreturn.append(user.balance)
            toreturn.append(user.theme)
            toreturn += list(reversed(user.notifications))
        except Exception as e:
            toreturn = ["Invalid Token, reload, if still broken, ask me", "0", str(type(e)), str(e)]
        save_data(project_id, userbytoken, users)
        return toreturn

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
            toreturn = user.transfer(int(amount), user2)
            save_data(project_id, userbytoken, users)
            return toreturn
        except:
            return "x"

    @client.request
    def set_theme(token, num):
        try:
            userbytoken[token].theme = num
            save_data(project_id, userbytoken, users)
        except:None
        return "k"

    @client.event
    def on_ready():
        print(f"Server for project {project_id} is running :D")

    # Start the client
    client.start(thread=True)
    return client

# Add projects
def add_project(project_id):
    if project_id not in projects:
        client = init_project(project_id)
        projects[project_id] = client
    else:
        print(f"Project {project_id} is already initialized.")

f = open("servelist.txt","r")
projects = f.read().splitlines()
f.close()
for project in projects:
    add_project(project)
