from statistics import mean
import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import time



"""
import stats, pandas, os

Code intakes CSVs and converts into pandas dataframes
records x and y value at y min for each csv

Finds the avg x value and shifts every min to that x value and 
shifts each corresponding point to the avg x value by adding the difference x+(x_avg-x_min) to x

Code outputs graph with multiple lines on it <-- profilometry data

"""
def main():
    start_time = time.perf_counter()
    directory = 'directory containing csvs'

    #print(directory)
    # csv_files = [pd.read_csv(f'{os.path.join(root, file)}') for root, dir, files in os.walk(directory) for file in files if file.endswith('.csv')]

    #csv_files = {file: pd.read_csv(f'{os.path.join(root, file)}') for root, dir, files in os.walk(directory) for file in files if file.endswith('.csv')}

    csv_files = [[pd.read_csv(f'{os.path.join(root, file)}'), re.sub(r'mms.*', 'mms', file)] for root, dir, files in os.walk(directory) for file in files if file.endswith('.csv')]


    # xmin_vals = [dataframe[0].loc[dataframe[0]['Height (µm)'].idxmin(),'Distance (µm)'] for dataframe in csv_files]

    xmin_vals_high_vel_load = [dataframe[0].loc[dataframe[0]['Height (µm)'].idxmin(),'Distance (µm)'] for dataframe in csv_files if '100mms' in dataframe[1] and '20N' in dataframe[1]]
    xmin_vals_high_vel_lo_load = [dataframe[0].loc[dataframe[0]['Height (µm)'].idxmin(),'Distance (µm)'] for dataframe in csv_files if '100mms' in dataframe[1] and '10N' in dataframe[1]]
    xmin_vals_low_vel_hi_load = [dataframe[0].loc[dataframe[0]['Height (µm)'].idxmin(),'Distance (µm)'] for dataframe in csv_files if '20mms' in dataframe[1] and '20N' in dataframe[1]]
    xmin_vals_low_vel_load = [dataframe[0].loc[dataframe[0]['Height (µm)'].idxmin(),'Distance (µm)'] for dataframe in csv_files if '20mms' in dataframe[1] and '10N' in dataframe[1]]

    # avg_x_high_vel_load = mean(xmin_vals_high_vel_load)
    # avg_x_high_vel_lo_load = mean(xmin_vals_high_vel_lo_load)
    # avg_x_low_vel_hi_load = mean(xmin_vals_low_vel_hi_load)
    # avg_x_low_vel_load = mean(xmin_vals_low_vel_load)

    avg_x_high_vel_load = 0
    avg_x_high_vel_lo_load = 0
    avg_x_low_vel_hi_load = 0
    avg_x_low_vel_load = 0

    high_speed_load_dfs = []
    low_speed_load_dfs = []
    hi_speed_lo_load_dfs = []
    lo_speed_hi_load_dfs = []

    index1 = 0
    index2 = 0
    index3 = 0
    index4 = 0

    #


    for dataframe in csv_files:
        dataframe[0]['Height (µm)'] = dataframe[0]['Height (µm)'] + (0 - dataframe[0]['Height (µm)'][0])
        if '100mms' in dataframe[1] and '20N' in dataframe[1]:
            dataframe[0]['Distance (µm)'] = dataframe[0]['Distance (µm)'] + (avg_x_high_vel_load - xmin_vals_high_vel_load[index1])
            high_speed_load_dfs.append([dataframe[0], dataframe[1]])
            index1 += 1

        elif '20mms' in dataframe[1] and '10N' in dataframe[1]:
            dataframe[0]['Distance (µm)'] = dataframe[0]['Distance (µm)'] + (avg_x_low_vel_load - xmin_vals_low_vel_load[index2])
            low_speed_load_dfs.append([dataframe[0], dataframe[1]])
            index2 += 1

        elif '100mms' in dataframe[1] and '10N' in dataframe[1]:
            dataframe[0]['Distance (µm)'] = dataframe[0]['Distance (µm)'] + (avg_x_high_vel_lo_load - xmin_vals_high_vel_lo_load[index3])
            hi_speed_lo_load_dfs.append([dataframe[0], dataframe[1]])
            index3 += 1

        elif '20mms' in dataframe[1] and '20N' in dataframe[1]:
            dataframe[0]['Distance (µm)'] = dataframe[0]['Distance (µm)'] + (avg_x_low_vel_hi_load - xmin_vals_low_vel_hi_load[index4])
            lo_speed_hi_load_dfs.append([dataframe[0], dataframe[1]])
            index4 += 1

    end_time = time.perf_counter() 
    print(f'Code completed in {end_time - start_time} seconds.')
    plot(high_speed_load_dfs, '100mm/s and 20N')
    plot(low_speed_load_dfs, '20mm/s and 10N')
    plot(hi_speed_lo_load_dfs, '100mm/s and 10N')
    plot(lo_speed_hi_load_dfs, '20mm/s and 20N')
#-------------------------------------------------------------------------------------------------------------

def plot(dataframes:list, graph_name:str):
    graph_name = f'{graph_name} Profilometry Depth Overlays'
    plt.title(graph_name)
    plt.xlabel('Distance (µm)')
    plt.ylabel('Height (µm)')
    for dataframe in dataframes:
        if '10N' in dataframe[1]:
            plt.plot(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'], '--', label=dataframe[1])
        elif '20N' in dataframe[1]:
            plt.plot(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'], label=dataframe[1])
    plt.legend(loc='upper right')
    plt.show()

    # version_number = 0

    # while version_number < 3:
    #     if not os.path.exists(directory path):
    #         os.mkdir(f'Graphs Ver {version_number}')
    #         path = 
    #         break
    #     else:
    #         version_number += 1
    
    # plt.savefig(f'{path}\\graph_name')

#----------------------------------------------------------------------------------------

    # create legend, same colours for each diff specification <-- mostly done
    #--change naming convention

    # create reference bar where all the graphs will dip down from
    # find points where slope between two pts are relatively low on edges <-- ignore points where slope is low b/w these points
    #--- go from left to right and then from right to left <-- should create a variable called slope sensitivity <-- determines how many pts included
    # averages the y values out for all these points and set that as reference for each graph
    # Use each reference to add or subtract values so that all of them are somewhat all on the same reference & can be differentiated

if __name__ =='__main__':
    main()