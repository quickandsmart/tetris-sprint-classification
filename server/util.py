import json
import pickle
import numpy as np
import requests
import pandas as pd
import math
import time
from datetime import datetime, timedelta

__scaler = None
__model = None
__api_request = None

def request_sprint_data(username):
    global __api_request
    url = f"https://ch.tetr.io/api/users/{username.lower()}/records"
    response = requests.get(url)
    if response.status_code == 200:
        if not pd.DataFrame(response.json()['data']['records']['40l']['record']).empty:
            __api_request = response

def get_replay():
    replay_id =  __api_request.json()['data']['records']['40l']['record']['replayid']
    replay_link = f"https://tetr.io/#r:{replay_id}"
    return replay_link

def get_sprint_data():
    sprint_data = pd.json_normalize(__api_request.json()['data']['records']['40l']['record']['endcontext'])
    return sprint_data

def classify_sprint(username):
    try:
        request_sprint_data(username)
    except:
        print("User doesn't exist or does not have a sprint")
        return
    sprint_data = get_sprint_data()
    sprint_data2 = sprint_data.drop(['level_lines', 'level_lines_needed', 'zenlevel',
                                     'zenprogress', 'level', 'currentcombopower', 'kills',
                                     'time.start', 'time.prev', 'time.frameoffset', 'gametype',
                                     'clears.minitspindoubles', 'clears.tspinquads', 'garbage.sent',
                                     'garbage.received', 'garbage.attack', 'garbage.cleared', 'currentbtbchainpower',
                                     'time.zero', 'time.locked', 'seed'], axis=1, errors='ignore')
    sprint_data2['KPP'] = sprint_data2.inputs / sprint_data2.piecesplaced
    sprint_data2['finalTime'] = sprint_data2['finalTime'] / 1000
    if 'holds' not in sprint_data2.columns:
        sprint_data2.insert(2, 'holds', 0)
    sprint_data3 = __scaler.transform(sprint_data2)
    prediction = __model.predict(sprint_data3)[0]
    return prediction





def load_saved_artifacts():
    print("loading saved artifacts...start")

    global __scaler
    with open("../Model/data_scaler.pickle", "rb") as f:
        __scaler = pickle.load(f)

    global __model
    if __model is None:
        with open('../Model/sprint_classification_model.pickle', 'rb') as f:
            __model = pickle.load(f)


    print("loading saved artifacts...done")


if __name__ == '__main__':
    load_saved_artifacts()
    print(classify_sprint('icly'))
    print(classify_sprint('quickandsmart'))
    print(classify_sprint('kiken'))
    print(classify_sprint('atombolders'))