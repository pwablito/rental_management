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

if __name__ == '__main__':
    app.run()
