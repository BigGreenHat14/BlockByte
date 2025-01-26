#yes i did partially use chatgpt thank you for asking - every dev in 2025

import pickle
import os
import scratchattach as sa
import requests
import bghsecrets
import math

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
    def __init__(self, uuid, name, password):
        self.uuid = uuid
        self.name = name
        self.theme = "56.7"
        self.balance = 100.0
        self.notifications = []
        self.password = password

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
    cloud = sa.get_tw_cloud(project_id, contact="@BigGreenHat on Scratch")
    client = cloud.requests()

    userbytoken, users = load_data(project_id)

    @client.request
    def login(username,password):
        try:
            user = userbytoken[users[username]]
            if user.password == password:
                return user.uuid
            else:
                return "x"
        except:
            return "x"

    @client.request
    def signup(username,password):
        print(users)
        if username in list(users.keys()):
            return "x"
        uuid = get_uuid()
        users[username] = uuid
        userbytoken[uuid] = User(uuid, username, password)
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

    # Leaderboard feature
    @client.request
    def leaderboard():
        try:
            leaderboard_data = sorted(userbytoken.values(), key=lambda u: u.balance, reverse=True)
            return [f"{user.name}: {user.get_balance()}" for user in leaderboard_data]
        except Exception as e:
            return f"{str(type(e))}: {str(e)}"
    # Find another user's balance
    @client.request
    def get_balance(othername):
        try:
            user = userbytoken[users[othername]]
            return str(user.get_balance())
        except:
            return "x"
    @client.event
    def on_ready():
        print(f"Server for project {project_id} is running :D")

    # Start the client
    client.start(thread=False)
    return client

# Set project
init_project(1116465685)
