# I wouldn't recommend looking through my code, for your sanity

class User:
    def __init__(self,uuid,name):
        self.uuid = uuid
        self.name = name
        self.balance = 100.0
        self.notifications = []
    def get_balance(self):
        return round(self.balance)
    def transfer(self,amount,recipient): # type: ignore
        if amount > self.balance or amount < 1:
            return "x"
        self.balance -= amount
        recipient.balance += amount
        recipient.notifications.append(f"{self.name} sent you {amount} BlockByte{'' if amount == 1 else 's'}!")
        return "k"

import pickle
import os
def save_data(userbytoken,users):
    f = open("blockbytedb","wb")
    f.write(pickle.dumps((userbytoken,users)))
def load_data():
    if os.path.exists("blockbytedb"):
        f = open("blockbytedb","rb")
        return pickle.loads(f.read())
    else:
        return ({},{})

import scratchattach as sa
from swear_provention import Filter
import requests
import bghsecrets
import math
session = sa.login(**bghsecrets.scratchlogin)
cloud = session.connect_tw_cloud("1116465685",contact=f"@{bghsecrets.scratchlogin["username"]} on Scratch")
client = cloud.requests()
userbytoken, users = load_data()
rooms = {}
connectedto = {}
def get_uuid():
    import uuid
    return str(uuid.uuid4())
@client.request
def login(token):
    try:
        return list(users.keys())[list(users.values()).index(token)]
    except:
        return "x"
@client.request
def signup(username):
    if username != Filter(username):
        return "b"
    if username in list(users.keys()):
        return "x"
    uuid = get_uuid()
    users[username] = uuid
    userbytoken[uuid] = User(uuid,username)
    save_data(userbytoken,users)
    return uuid
@client.request
def info(token):
    try:
        toreturn = []
        user = userbytoken[token]
        toreturn.append(user.balance)
        toreturn += list(reversed(user.notifications))
    except:
        toreturn = ["Invalid Token, please notify me","pls restart"]
    save_data(userbytoken,users)
    return toreturn
@client.request
def dismiss(token):
    userbytoken[token].notifications = []
    save_data(userbytoken,users)
    return "k"
@client.request
def transfer(token,othername,amount):
    try:
        user = userbytoken[token]
        user2 = userbytoken[users[othername]]
        toreturn = user.transfer(int(amount),user2)
        save_data(userbytoken,users)
        return toreturn
    except:
        return "x"
@client.event
def on_ready():
    print("gerbert da serber is run :D")
client.start(thread=False)
