#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
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
                        id = file.split(".")[0]
                        with open(file_path + "/" + file, "rb") as img:
                            data = base64.b64encode(img.read())
                            img.close()
                        img_json = {
                            "id": id,
                            "data": "data:image/jpeg;base64, " + data.decode("utf-8")
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

def save_image(image_data, event_token):
    with open (f"{app_dir}/config.json", "r") as config_file:
        json_data = json.load(config_file)
        file_path = json_data["file_path"]

        if not os.path.exists(file_path + event_token + "/"):
            os.makedirs(file_path + event_token + "/")

        header, encoded = image_data.split(",", 1)
        image_data = base64.urlsafe_b64decode(encoded)
        image_file = io.BytesIO(image_data)
        image = Image.open(image_file)

        date = functions.get_iso_8601_date_time()
        random_string = functions.generate_random_string(12)
        string_to_hash = event_token + date + random_string
        encoded_string = string_to_hash.encode('utf-8')
        file_name = hashlib.sha256(encoded_string).hexdigest()

        image.save(file_path + event_token + "/" + file_name + ".webp")

def submit_photos(auth_token, event_token, image_json):
    with open (f"{app_dir}/config.json", "r") as config_file:
        json_data = json.load(config_file)
        if auth_token == json_data["auth_token"]:
            #try:
                #image_data = json.load(image_json)
                for image in image_json:
                    with open('/Users/bradleyashlock/Documents/photo_app_backend/test.txt', "w") as test:
                        test.write(image[0])
                    save_image(image[0], event_token)
            #except Exception as e:
            #    print(f"There was an error submitting new photos. Error: {e}")
        else:
            return print("Authorization token is not valid...")