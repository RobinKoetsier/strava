from math import floor 
import datetime
import numpy as np


def add_pace(row):
    minutes =  floor((60/row['average_speed']) % 60)
    seconds = floor((60/row['average_speed'] * 60) % 60)
    if seconds < 10:
        seconds = f'0{seconds}'
    return str(f'{minutes}:{seconds}')

def add_pace_total(row):
    minutes =  floor((60/row['total']) % 60)
    seconds = floor((60/row['total'] * 60) % 60)
    if seconds < 10:
        seconds = f'0{seconds}'
    return str(f'{minutes}:{seconds}')

def get_last_run(activities):
    last_run = activities.iloc[0, :]
    pace = add_pace(last_run)
    distance = last_run['distance']
    timesec = floor(last_run['moving_time'])
    time = str(datetime.timedelta(seconds=timesec))
    return f'Pace:\n{pace}\nDistance:\n{distance}\nTime:\n{time}'
    


def get_all_runs(activities):
    activities['total'] = np.sum(activities['distance'])/np.sum(activities['moving_time'])*3600
    row = activities.iloc[0, :]
    pace = add_pace_total(row)
    distance = round(np.sum(activities['distance']),2)
    timesec = floor(np.sum(activities['moving_time']))
    time = str(datetime.timedelta(seconds=timesec))
    return f'Pace:\n{pace}\nDistance:\n{distance}KM\nTime:\n{time}'



