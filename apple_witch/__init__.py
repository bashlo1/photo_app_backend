#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from flask_cors import CORS
from PIL import Image
import sys, os, hashlib

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)

#helpers
import apple_witch.helpers.functions as functions
import apple_witch.helpers.site_responses as site_responses

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'c:/Users/Bradley/Pictures/Wedding'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUTHORIZATION'] = "2`LMZ;h+rs1y_s@j"

@app.route("/app", methods=["POST", "GET"])
def receive_post():
    print(request.method)
    if request.method == "POST":
        if request.headers["Topic"] == "images/add":
            if 'image' not in request.files:
                return 'message: No image part', 400

            file = request.files['image']

            if file.filename == '':
                return 'message: No selected file', 400

            if file and request.headers["Auth-Token"] == app.config['AUTHORIZATION']:
                site_responses.save_photo(request, file, app.config['UPLOAD_FOLDER'])

                return 'message: Image uploaded successfully', 200

            return 'message: Image upload failed', 500
    
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
    app.run(host="10.0.0.12", port="8080", debug=True, use_reloader=True)