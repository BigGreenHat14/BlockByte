#yes i did partially use chatgpt thank you for asking - every dev in 2025

import pickle
import os
import scratchattach as sa
import requests
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
    cloud = sa.get_tw_cloud(project_id,purpose="Blockbyte Server", contact="@BigGreenHat on Scratch")
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
            toreturn.append(list(userbytoken.values()).index(user))
            toreturn += list(reversed(user.notifications))
        except Exception as e:
            toreturn = ["Invalid Token, reload, if still broken, ask me", "0", "0", str(type(e)), str(e)]
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

def bbshell_mm():
    try:
        while True:
            exec(input ("BB >>> "))
    except:
        return
def bbshell():
    version = 0.2
    print(f"Blockbyte Shell v{str(version)}")
    print("Before using, make sure blockbyte is not running!")
    print("")
    pid = input("Enter project ID > ")
    userbytoken, users = load_data(int(pid))
    shell = not ("-c" in sys.orig_argv)
    while True:
        print("0. Exit")
        print("1. Manual mode")
        print("2. Reset token")
        print("")
        match input("Enter Number > "):
            case 0:
                save_data(pid,usersbytoken,users)
                sys.exit(0)
            case 1:
                bbshell_mm()
            case 2:
                import copy
                names = list(users.keys())
                print(dict(enumerate(names)))
                accindex = int(input("Enter Account Index > "))
                olduuid = users[names[accindex]]
                uuid = get_uuid()
                userbytoken[olduuid].uuid = uuid
                users[names[accindex]] = uuid
                usersbytoken[uuid] = copy.copy(userbytoken[olduuid])
                del userbytoken[olduuid]
        save_data(pid,usersbytoken,users)
# Set project
if __name__ == "__main__":
   init_project(1116465685)
else:
    bbshell()
