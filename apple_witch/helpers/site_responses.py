#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageOps
import sys, os, json, base64, hashlib
import io, base64, os

app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(app_dir)

#helpers
import apple_witch.helpers.functions as functions

def get_config_data(auth_token, event_token):
    with open (f"{app_dir}/config.json", "r") as config_file:
        json_data = json.load(config_file)
        if auth_token == json_data["auth_token"]:
            try:
                event_info = json_data["keys"][event_token]
                return event_info
            except:
                return "error"
        else:
            return "error"

def is_image_file(file):
    try:
        with Image.open(file) as image:
            image.verify()
            return True
    except (IOError, SyntaxError):
        return False

def get_images(auth_token, event_token):
    with open (f"{app_dir}/config.json", "r") as config_file:
        json_data = json.load(config_file)
        if auth_token == json_data["auth_token"]:
            try:
                file_path = json_data["file_path"] + event_token
                if os.path.exists(file_path):
                    files = os.listdir(file_path)
                    image_data = []
                    for file in files:
                        if is_image_file(file_path + "/" + file):
                            id = file.split(".")[0]
                            with open(file_path + "/" + file, "rb") as img:
                                data = base64.b64encode(img.read())
                                img.close()
                            img_json = {
                                "id": id,
                                "data": "data:image/webp;base64, " + data.decode("utf-8")
                            }
                            image_data.append(img_json)
                    return image_data
                else:
                    os.makedirs(file_path)
                    print("Event image path does not exist...")
                    return []
            except Exception as e:
                print(f"There was an error getting the images. Error: {e}")
                return []
        else:
            print("Authorization token is not valid...")
            return []

def optimize_image(file):
    max_dimensions = (500, 500)

    image = Image.open(file)
    image.thumbnail(max_dimensions)
    image = ImageOps.exif_transpose(image)

    return image

def save_photo(request, file, UPLOAD_FOLDER):
    date = functions.get_iso_8601_date_time()
    random_string = functions.generate_random_string(12)
    string_to_hash = request.headers["Event-Token"] + date + random_string
    encoded_string = string_to_hash.encode('utf-8')
    file_name = hashlib.sha256(encoded_string).hexdigest()
    output_path = os.path.join(UPLOAD_FOLDER, request.headers["Event-Token"] ,file_name + "_" + file.filename)

    image = optimize_image(file)
    image.save(output_path, optimize=True, quality=95)