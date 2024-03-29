import requests
import pandas as pd
import polyline
#from keys import payload
import streamlit as st
"""
imports payload with following structure:
payload = {
        'client_id': <client id>,
        'client_secret': <client secret>,
        'refresh_token': <refresh token>,
        'grant_type': "refresh_token",
        'f': 'json'
    }
"""

payload = {
        'client_id': st.secrets["client_id"],
        'client_secret': st.secrets['client_secret'],
        'refresh_token': st.secrets['refresh_token'],
        'grant_type': "refresh_token",
        'f': 'json'
    }

def authorize_and_get_data():
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    
    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}
    my_dataset = []
    for i in range(1,5):
        print(i)
        param = {'per_page': 200, 'page': i}
        dataset_temp = requests.get(activites_url, headers=header, params=param).json()
        my_dataset = my_dataset + dataset_temp
    return my_dataset

def clean_data(my_dataset):
    activities = pd.json_normalize(my_dataset)
    activities['map.polyline'] = activities['map.summary_polyline'].apply(polyline.decode)

    # convert data types
    activities.loc[:, 'start_date'] = pd.to_datetime(activities['start_date']).dt.tz_localize(None)
    activities.loc[:, 'start_date_local'] = pd.to_datetime(activities['start_date_local']).dt.tz_localize(None)# convert values
    activities.loc[:, 'distance'] /= 1000 # convert from m to km
    activities.loc[:, 'average_speed'] *= 3.6 # convert from m/s to km/h
    activities.loc[:, 'max_speed'] *= 3.6 # convert from m/s to km/h# set index
    activities.set_index('start_date_local', inplace=False)# drop columns
    activities.drop(
        [
            'map.summary_polyline',
            'resource_state',
            'external_id',
            'upload_id',
            'location_city',
            'location_state',
            'has_kudoed',
            'start_date',
            'athlete.resource_state',
            'utc_offset',
            'map.resource_state',
            'athlete.id',
            'visibility',
            'heartrate_opt_out',
            'upload_id_str',
            'from_accepted_tag',
            'map.id',
            'manual',
            'private',
            'flagged',
        ],
        axis=1,
        inplace=True
    )
    return activities
