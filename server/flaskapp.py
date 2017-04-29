from flask import Flask
from flask import request
from telegramapp import the_game
import roboy_interface
import json
import sys
from logs import log
app = Flask(__name__)

def outp(text:str):
    print(text, file=sys.stderr)

@app.route("/")
def hello():
    return "Hello World!"

class RUpdate:
    def __init__(self, idict):
        self.type = idict["type"]
        self.data = idict["data"]

def make_rupdate(utype, data):
    return RUpdate({"type":utype, "data":data})

class RUpdates:
    def __init__(self, idict):
        self.ok = idict["ok"]
        if self.ok:
            self.updates = [RUpdate(up) for up in idict["updates"]]

@app.route("/sendUpdates", methods=['POST'])
def send_updates():
    #outp(json.dumps(request.get_json()))
    updates = RUpdates(request.get_json())
    if not updates.ok:
        return "update_not_ok"
    process_updates(updates.updates)
    return "ok"


def process_updates(updates):
    for update in updates:
        the_game.dm.set_data(update.type, update.data)
        log.info("UPDATE: {name}:{data}".format(name = update.type, data = json.dumps(update.data)))
    return "ok"


@app.route("/logs")
def logs():
    with open('logs/log.txt') as f:
        return f.read().replace("\n", "<br/>")