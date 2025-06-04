#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
import sys, os

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)

#helpers
import apple_witch.helpers.functions as functions
import apple_witch.helpers.site_responses as site_responses

app = Flask(__name__)

@app.route("/")
@app.route("/app/", methods=["POST", "GET"])
def receive_post():
    print(request.method)
    if request.method == "POST":
        if "Topic" in request.headers:
            if request.headers["Topic"] == "images/add":
                site_responses.submit_photos(request.headers["Auth-Token"], request.headers["Event-Token"], request.json)
                return "success", 200
        else:
            abort(400)
    elif request.method == "GET":
        if "Topic" in request.headers:
            if request.headers["Topic"] == "config/get":
                response_data = site_responses.get_config_data(request.headers["Auth-Token"], request.headers["Event-Token"])
                return response_data, 200
            
            if request.headers["Topic"] == "images/get":
                response_data = site_responses.get_images(request.headers["Auth-Token"], request.headers["Event-Token"])
                return response_data, 200
        else:
            abort(400)
    else:
        #log
        functions.submit_activity_log(request.method, str(request.headers).replace("\r", "").replace("\n", ", "), "", str(request.json))
        abort(400)

if __name__ == "__main__":
    app.run(host="10.1.1.37", port="8080", debug=True, use_reloader=True)