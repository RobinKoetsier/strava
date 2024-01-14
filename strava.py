import start
import helpers
import datetime
import urllib3
import numpy as np
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

this_year = datetime.date.today().year
last_year = this_year - 1
my_dataset = start.authorize_and_get_data()
activities = start.clean_data(my_dataset)

run_activities = activities[(activities['type'] == 'Run')]

run_activities_this_year = run_activities[(run_activities['start_date_local'] > datetime.datetime.strptime(f'31-12-{this_year-1}',"%d-%m-%Y"))]
run_activities_last_year = run_activities[(run_activities['start_date_local'] > datetime.datetime.strptime(f'31-12-{last_year-1}',"%d-%m-%Y")) & (run_activities['start_date_local'] < datetime.datetime.strptime(f'01-01-{this_year}',"%d-%m-%Y"))]

last_run = helpers.get_last_run(run_activities)
all_runs = helpers.get_all_runs(run_activities)
all_runs_last_year = helpers.get_all_runs(run_activities_last_year)


# Reverse rows using iloc() Function
run_activities_last_year_reverse = run_activities_last_year.iloc[::-1]
run_activities_last_year_reverse['total'] = np.cumsum(run_activities_last_year_reverse['distance'])

run_activities_reverse = run_activities.iloc[::-1]
run_activities_reverse['total'] = np.cumsum(run_activities_reverse['distance'])

ride_longitudes = [coordinate[1] for coordinate in run_activities['map.polyline'][0]]
ride_latitudes = [coordinate[0] for coordinate in run_activities['map.polyline'][0]]
fig, ax = plt.subplots()
ax.plot(ride_longitudes,ride_latitudes,'r-', alpha=1,color="blue")
plt.axis('off') 
plt.style.use('dark_background')
plt.show()

all_ride_longitudes = []
all_ride_latitudes = []
fig, ax = plt.subplots()
for map in run_activities['map.polyline']:
    ride_longitudes = [coordinate[1] for coordinate in map]
    ride_latitudes = [coordinate[0] for coordinate in map]
    if 4.637 < np.mean(ride_longitudes) < 4.919:
        if 51.450 < np.mean(ride_latitudes) < 51.657:
            all_ride_latitudes += ride_latitudes
            all_ride_longitudes += ride_longitudes
            ax.plot(ride_longitudes,ride_latitudes,'r-', alpha=1,color="blue")



plt.axis('off') 
plt.style.use('dark_background')
plt.show()