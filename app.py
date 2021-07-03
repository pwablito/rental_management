#!/usr/bin/env python3

from flask import Flask, redirect
import api.api

app = Flask(__name__, static_url_path="", static_folder="client/dist")

app.add_url_rule('/api/register', view_func=api.api.register, methods=["POST"])
app.add_url_rule('/api/login', view_func=api.api.login, methods=["POST"])

@app.route('/')
def index():
    return redirect("/index.html", code=302)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
