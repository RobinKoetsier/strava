import streamlit as st
import datetime
import start
import helpers
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Set your Strava API credentials
CLIENT_ID = '119119'
CLIENT_SECRET = 'b5bf66e3e833464b266c4b985d9c64de65948624'
REDIRECT_URI = 'http://localhost:8501/'

# Initialize Strava API client
this_year = datetime.date.today().year
last_year = this_year - 1

# Streamlit app
def main():
    st.title("Strava Data")

    # Authenticate with Strava
    # Authenticate with Strava
    auth_button = st.button("Authenticate and get data from Strava")
    if auth_button:
        my_dataset = start.authorize_and_get_data()
        activities = start.clean_data(my_dataset)
        # Retrieve Strava data button
        # st.header("Strava Data Per Year")
        run_activities = activities[(activities['type'] == 'Run')]
        # Get activities
        st.subheader('What do you want to see?')
        run_activities = activities[(activities['type'] == 'Run')]
        run_activities_this_year = run_activities[(run_activities['start_date_local'] > datetime.datetime.strptime(f'31-12-{this_year-1}',"%d-%m-%Y"))]
        run_activities_last_year = run_activities[(run_activities['start_date_local'] > datetime.datetime.strptime(f'31-12-{last_year-1}',"%d-%m-%Y")) & (run_activities['start_date_local'] < datetime.datetime.strptime(f'01-01-{this_year}',"%d-%m-%Y"))]
        run_activities_2022 = run_activities[(run_activities['start_date_local'] > datetime.datetime.strptime(f'31-12-{last_year-2}',"%d-%m-%Y")) & (run_activities['start_date_local'] < datetime.datetime.strptime(f'01-01-{last_year}',"%d-%m-%Y"))]

        last_run = helpers.get_last_run(run_activities).split('\n')
        all_runs = helpers.get_all_runs(run_activities).split('\n')
        all_runs_last_year = helpers.get_all_runs(run_activities_last_year).split('\n')
        all_runs_this_year = helpers.get_all_runs(run_activities_this_year).split('\n')
        all_runs_2022 = helpers.get_all_runs(run_activities_2022).split('\n')
        df = pd.DataFrame(
    [   
        {"Type": "Last run", "pace": last_run[1], "distance": last_run[3], "Time": last_run[5]},
        {"Type": "2024","pace": all_runs_this_year[1], "distance": all_runs_this_year[3], "Time": all_runs_this_year[5]},
        {"Type": "2023","pace": all_runs_last_year[1], "distance": all_runs_last_year[3], "Time": all_runs_last_year[5]},
        {"Type": "2022","pace": all_runs_2022[1], "distance": all_runs_2022[3], "Time": all_runs_2022[5]},
        {"Type": "All runs","pace": all_runs[1], "distance": all_runs[3], "Time": all_runs[5]},
        
    ]
)
        tab1_1, tab1_2, tab1_3, tab1_4 = st.tabs(["Last Run", "Totals 2024", "Totals 2023", "Totals"])
        
        with tab1_1:

            ride_longitudes = [coordinate[1] for coordinate in run_activities['map.polyline'][0]]
            ride_latitudes = [coordinate[0] for coordinate in run_activities['map.polyline'][0]]
            fig, ax = plt.subplots()
            ax.plot(ride_longitudes,ride_latitudes,'r-', alpha=1,color="blue")
            plt.axis('off') 
            plt.style.use('dark_background')
            st.pyplot(fig,clear_figure=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(last_run[0])
                st.write(f'{last_run[1]} min/km')

            with col2:
                st.write(last_run[2])
                st.write(last_run[3])

            with col3:
                st.write(last_run[4])
                st.write(last_run[5]) 

        with tab1_2:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(all_runs_this_year[0])
                st.write(f'{all_runs_this_year[1]} min/km')

            with col2:
                st.write(all_runs_this_year[2])
                st.write(all_runs_this_year[3])

            with col3:
                st.write(all_runs_this_year[4])
                st.write(all_runs_this_year[5]) 
                
        with tab1_3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(all_runs_last_year[0])
                st.write(f'{all_runs_last_year[1]} min/km')

            with col2:
                st.write(all_runs_last_year[2])
                st.write(all_runs_last_year[3])

            with col3:
                st.write(all_runs_last_year[4])
                st.write(all_runs_last_year[5]) 

        with tab1_4:
                        
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
            st.pyplot(fig)
            st.dataframe(df, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(all_runs[0])
                st.write(f'{all_runs[1]} min/km')

            with col2:
                st.write(all_runs[2])
                st.write(all_runs[3])

            with col3:
                st.write(all_runs[4])
                st.write(all_runs[5]) 


      
        
    

    
if __name__ == "__main__":
    main()
