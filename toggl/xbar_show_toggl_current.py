#!/Users/yurikohashizume/.pyenv/versions/3.8.0/bin/python
# coding : UTF-8

import requests
import time
import datetime
from datetime import datetime as dt
from datetime import timedelta, timezone
from requests.auth import HTTPBasicAuth

API_TOKEN = {token_id}


def get(section: str):
    response = requests.get(
       'https://api.track.toggl.com/api/v8/{}'.format(section),
       auth=HTTPBasicAuth(API_TOKEN,'api_token')
    )
    data = response.json()['data']

    return data

entry = get("time_entries/current") 

if entry:
    description = entry['description'] if entry['description'] else "(no description)"

    start_time = dt.strptime(entry['start'],"%Y-%m-%dT%H:%M:%S%z")
    duration = dt.now(datetime.timezone(datetime.timedelta(hours=-9))) - start_time
    duration_h = duration.seconds//3600
    duration_m = duration.seconds//60 - duration_h*60

    project_name = ""
    options = "color=blue"
    if "pid" in entry.keys():
        project = get("projects/{}".format(entry['pid']))
        project_name = project["name"]
        options = "color=".format(project['hex_color'])
        
    print("{} {} {} {}h {}m | {}".format(chr(int(0x23f3)),description, project_name, duration_h, duration_m, options).replace('0h ',''))
else:
    print("Toggl not running | color=red")

