from flask import Flask
import json

app = Flask(__name__, static_folder=None)

@app.route("/api/test")
def hello_world():
    return json.dumps({"success":True})
