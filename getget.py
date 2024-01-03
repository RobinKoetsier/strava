import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import polyline
import pandas as pd
import tqdm
import numpy as np
import folium 
from math import floor
import matplotlib.pyplot as plt

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "119119",
    'client_secret': 'b5bf66e3e833464b266c4b985d9c64de65948624',
    'refresh_token': "7574f747531e2f9fd3e296d540baffc0e86beb8e",
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset[0]["name"])
print(my_dataset[0])
print(len(my_dataset))
print(my_dataset[0]["map"]["summary_polyline"])

# add decoded summary polylines

activities = pd.json_normalize(my_dataset)
activities['map.polyline'] = activities['map.summary_polyline'].apply(polyline.decode)




# convert data types
activities.loc[:, 'start_date'] = pd.to_datetime(activities['start_date']).dt.tz_localize(None)
activities.loc[:, 'start_date_local'] = pd.to_datetime(activities['start_date_local']).dt.tz_localize(None)# convert values
activities.loc[:, 'distance'] /= 1000 # convert from m to km
activities.loc[:, 'average_speed'] *= 3.6 # convert from m/s to km/h
activities.loc[:, 'max_speed'] *= 3.6 # convert from m/s to km/h# set index
activities.set_index('start_date_local', inplace=True)# drop columns
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

# activities = activities[(activities['start_date_local'] > '01-01-2023') & (activities['type'] == 'Run')] 
activities = activities[(activities['type'] == 'Run')] 
def add_pace(row):
    minutes =  floor((60/row['average_speed']) % 60)
    seconds = floor((60/row['average_speed'] * 60) % 60)
    if seconds < 10:
        seconds = f'0{seconds}'
    return str(f'{minutes}:{seconds}')

activities['pace'] = activities.apply(add_pace, axis=1)

def add_pace_total(row):
    minutes =  floor((60/row['total']) % 60)
    seconds = floor((60/row['total'] * 60) % 60)
    if seconds < 10:
        seconds = f'0{seconds}'
    return str(f'{minutes}:{seconds}')

activities['total'] = np.sum(activities['distance'])/np.sum(activities['moving_time'])*3600
activities['pace_total'] = activities.apply(add_pace_total, axis=1)
activities





# select one activity
my_ride = activities.iloc[0, :] # first activity (most recent)# plot ride on map
centroid = [
    np.mean([coord[0] for coord in my_ride['map.polyline']]), 
    np.mean([coord[1] for coord in my_ride['map.polyline']])
]
m = folium.Map(location=centroid, zoom_start=10)
folium.PolyLine(my_ride['map.polyline'], color='red').add_to(m)

display(m)


plt.scatter(x=[coord[0] for coord in my_ride['map.polyline']], y=[coord[1] for coord in my_ride['map.polyline']])
plt.plot([coord[0] for coord in my_ride['map.polyline']], [coord[1] for coord in my_ride['map.polyline']],'b')
xcor=[coord[0] for coord in my_ride['map.polyline'] ]
ycor=[coord[1] for coord in my_ride['map.polyline']] 
plt.plot(ycor,xcor,'b')
plt.show()


all_coord = []
for run in activities['map.polyline']:
    all_coord.append(run)
    xcor=[coord[0] for coord in run]
    ycor=[coord[1] for coord in run]
    if 51 < np.mean(xcor) < 51.8:
        if 4.7 < np.mean(ycor) < 4.8:
            plt.plot(ycor,xcor,'b')
    else:
        print(xcor)
plt.show()

activities['start_date_local'] = activities.index
rslt_df = activities[(activities['start_date_local'] > '01-01-2023') & (activities['type'] == 'Run')] 

print(activities['type'].unique())
type(activities['sport_type'])


round(np.sum(activities['distance']),2)
round(np.sum(rslt_df['distance']),2)

round(np.sum(activities['distance']),2)
round(np.sum(rslt_df['distance']),2)

(rslt_df['moving_time']/60) / rslt_df['distance']


activities.columns


minutes = floor((60/activities['average_speed'][0]) % 60)
seconds = floor((60 / activities['average_speed'][0] * 60) % 60)
f'Pace: {minutes}:{seconds}'





activities['minutes'] = floor((60/activities['average_speed']) % 60)
seconds = floor((60 / activities['average_speed'][0] * 60) % 60)
f'Pace: {minutes}:{seconds}'



# define function to get elevation data using the open-elevation API
def get_elevation(latitude, longitude):
    base_url = 'https://api.open-elevation.com/api/v1/lookup'
    payload = {'locations': f'{latitude},{longitude}'}
    r = requests.get(base_url, params=payload).json()['results'][0]
    return r['elevation']# get elevation data
elevation_data = list()
for idx in tqdm(activities.index):
    activity = activities.loc[idx, :]
    elevation = [get_elevation(coord[0], coord[1]) for coord in activity['map.polyline']]
    elevation_data.append(elevation)# add elevation data to dataframe
activities['map.elevation'] = elevation_data