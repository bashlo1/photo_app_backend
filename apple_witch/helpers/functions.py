from datetime import datetime, timedelta
import sys, os, json
import random
import string

app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(app_dir)

def get_date():
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    return formatted_date

def get_date_time():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date

def get_iso_8601_date_time():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S.000z")
    return formatted_date

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def submit_activity_log(activity, info, response_status, response_content):
    date = get_date()
    date_time = get_date_time()
    log = date_time + "|" + activity + "|" + info + "|" + response_status + "|" + response_content + "\n"
    with open(f'{app_dir}/apple_witch/logs/{date}.log', 'a', encoding='utf-8') as f:
        f.write(log)