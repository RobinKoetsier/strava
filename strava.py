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
run_activities_this_year = run_activities[(run_activities['start_date_local'] > f'31-12-{this_year-1}')]
run_activities_last_year = run_activities[(run_activities['start_date_local'] > f'31-12-{last_year-1}')]

last_run = helpers.get_last_run(run_activities)
all_runs = helpers.get_all_runs(run_activities)
all_runs_last_year = helpers.get_all_runs(run_activities_last_year)


# Reverse rows using iloc() Function
run_activities_last_year_reverse = run_activities_last_year.iloc[::-1]
run_activities_last_year_reverse['total'] = np.cumsum(run_activities_last_year_reverse['distance'])

run_activities_reverse = run_activities.iloc[::-1]
run_activities_reverse['total'] = np.cumsum(run_activities_reverse['distance'])

import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.axes()
x = run_activities_last_year_reverse['total']
y= run_activities_last_year_reverse['start_date_local']
ax.plot(y,x,color="red")
x = run_activities_reverse['total']
y= run_activities_reverse['start_date_local']
ax.plot(y,x,color="black")
#plt.axis('off')
plt.show()
#plt.savefig("test.png", bbox_inches='tight')


