#!/usr/bin/env python3

from flask import Flask, redirect
import api.api
import requests

app = Flask(__name__)

app.add_url_rule('/api/register', view_func=api.api.register, methods=["POST"])
app.add_url_rule('/api/login', view_func=api.api.login, methods=["POST"])
app.add_url_rule('/api/update_user', view_func=api.api.update_user, methods=["POST"])
app.add_url_rule('/api/get_listings', view_func=api.api.get_listings, methods=["POST"])

@app.route('/')
def index():
    return redirect("/index.html", code=302)

@app.route('/<path:path>')
def proxy(path):
  return requests.get(f'http://localhost:8080/{path}').content

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
