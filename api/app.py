#!/usr/bin/env python3

from flask import Flask, redirect
import api
import requests
import os

app = Flask(__name__)

app.add_url_rule('/api/register', view_func=api.register, methods=["POST"])
app.add_url_rule('/api/login', view_func=api.login, methods=["POST"])
app.add_url_rule('/api/update_user', view_func=api.update_user, methods=["POST"])
app.add_url_rule('/api/get_listings', view_func=api.get_listings, methods=["POST"])
app.add_url_rule('/api/create_listing', view_func=api.create_listing, methods=["POST"])
app.add_url_rule('/api/delete_listing', view_func=api.delete_listing, methods=["POST"])
app.add_url_rule('/api/delete_user', view_func=api.delete_user, methods=["POST"])
app.add_url_rule('/api/get_users', view_func=api.get_users, methods=["POST"])
app.add_url_rule('/api/update_user', view_func=api.update_user, methods=["POST"])
app.add_url_rule('/api/create_user', view_func=api.create_user, methods=["POST"])
app.add_url_rule('/api/update_listing', view_func=api.update_listing, methods=["POST"])

### FOR DEVELOPMENT SERVER ###
@app.route('/')
def index():
    return redirect("/index.html", code=302)

@app.route('/<path:path>')
def proxy(path):
  return requests.get(f'http://localhost:8080/{path}').content
### END DEVELOPMENT SERVER ###

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
