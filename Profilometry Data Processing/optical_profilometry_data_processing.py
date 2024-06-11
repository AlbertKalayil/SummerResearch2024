#from statistics import mean
import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import time
from scipy import integrate as intg
from statistics import mean, stdev
#--------------------------------------------------------------------------------------------------------------
"""
import stats, pandas, os

Code intakes CSVs and converts into pandas dataframes
records x and y value at y min for each csv

Finds the avg x value and shifts every min to that x value and 
shifts each corresponding point to the avg x value by adding the difference x+(x_avg-x_min) to x

Code outputs graph with multiple lines on it <-- profilometry data

"""
#--------------------------------------------------------------------------------------------------------------
def main():
    start_time = time.perf_counter() # Credits @LiamPond
    directory = 'C:\\Users\\alber\\OneDrive - University of Calgary\\2024Tribometer\\Optical Profilometry Data\\Profilm CSVs'
    
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

    # TODO Average out first ten data points for each graph and move that average to 0
    for dataframe in csv_files:
        # dataframe[0]['Height (µm)'] = dataframe[0]['Height (µm)'] + (0 - dataframe[0]['Height (µm)'][0])
        dataframe[0]['Height (µm)'] = dataframe[0]['Height (µm)'] - mean(dataframe[0]['Height (µm)'][:20])
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

    end_time = time.perf_counter() # Credits @LiamPond
    print(f'Code executed in {end_time - start_time} seconds.') # Credits @LiamPond
    
    #----------------------------------------------------------------------------------Save Plot begins
    # version_number = 0
    # base_path = 'C:\\Users\\alber\\OneDrive - University of Calgary\\2024Tribometer\\Optical Profilometry Data\\Oils\\Graphs\\'

    # while version_number < 4:
    #     new_path = f'{base_path}Graphs Ver {version_number}'
    #     if not os.path.exists(new_path):
    #         os.mkdir(new_path)
    #         break
    #     else:
    #         version_number += 1

    # plot(high_speed_load_dfs, '100mm/s and 20N', new_path)
    # plot(low_speed_load_dfs, '20mm/s and 10N', new_path)
    # plot(hi_speed_lo_load_dfs, '100mm/s and 10N', new_path)
    # plot(lo_speed_hi_load_dfs, '20mm/s and 20N', new_path)

    #------------------------------------------------------------------------------------Save Plot ends
    #Show Plot begins

    dataframes_dict = {'100mm/s and 20N':high_speed_load_dfs, '20mm/s and 10N':low_speed_load_dfs, '100mm/s and 10N': hi_speed_lo_load_dfs, '20mm/s and 20N':lo_speed_hi_load_dfs}

    area_vol = ['Area', 'Volume']

    # for (key, value) in dataframes_dict.items():
    #     plot(value, key)

    #------------------------------------------------------------------------------------
    #Show Grouped Bar Chart
    grouped_bar_dict_main = {}
    oil_names = []
    for (key, value) in dataframes_dict.items():
        grouped_bar_dict_main.update(area_integral(value, key)[2]) # Just considering wear vol
        oil_names = area_integral(value, key)[3]

    # Plotting Group Bar Graph
    grouped_bar_df = pd.DataFrame(grouped_bar_dict_main)
    grouped_bar_df.index = oil_names
    plt.rc('axes', linewidth=3) # sets width of axes
    grouped_bar_df.plot(kind='bar', figsize=(14,9))
    plt.xlabel('Oil Name', fontsize=15, fontweight='bold')
    plt.ylabel('Wear Volume µm Cubed', fontsize=15, fontweight='bold')
    plt.tick_params(axis='both', which='major', labelsize=15, width=3)
    plt.xticks(fontweight='bold', rotation=0)
    plt.yticks(fontweight='bold')
    plt.title('Wear Volume for Different Parameters in Varying Oil Concentration', fontsize=18, fontweight='bold')
    plt.legend(loc='upper right', prop={'weight': 'bold', 'size': 12}, frameon=False)
    plt.show()

    #------------------------------------------------------------------------------------
    # Area Integral and Volume Calculations

    for i in range(len(area_vol)):
        print('-----------------------------------------------------')
        for (key, value) in dataframes_dict.items():
            print(f'{area_vol[i]}s for {key} Graph: \n{area_integral(value, key)[i]}\n\n')
        print('-----------------------------------------------------')

    #Show Plot ends

#-------------------------------------------------------------------------------------------------------------

def user_interface(): # still a work in progress
    print('Welcome to the file which produces Profilometry Overlay Graphs and the CSV data from ProfilmOnline. \
          This software can autoimport CSV files from a directory of your choosing, plot each overlay graph for one combination of parameters \
          and save all the files to a directory of your choosing.')
    user_directory = input('Input the EXACT file path of the directory containing the CSVs that you want to process: \n')
    user_parameters = input('\nInput the total number of parameters, parameters should be force and speed only, otherwise change this code\n')
    user_show_graphs = input('\nWould you like to see the graphs? y/n \n')
    user_save_image = input('\nWould you like to save the graphs in a folder? y/n \n')
    user_areas = input('\nWould you like to see the positive area (area of all the bumps) and negative area (area of all the holes)? y/n \n')
    pass


#--------------------------------------------------------------------------------------------------------------

def plot(dataframes:list, graph_name:str): 
# def plot(dataframes:list, graph_name:str, new_path:str):
    graph_name = f'{graph_name} Profilometry Depth Overlays'
    plt.rc('axes', linewidth=3) # sets width of axes
    plt.figure(figsize=(14,9))
    plt.title(graph_name, fontsize=18,fontweight='bold')
    plt.tick_params(axis='both', which='major', labelsize=15, width=3)
    plt.xticks(fontweight='bold')
    plt.yticks(fontweight='bold')
    plt.xlabel('Distance (µm)', fontsize=15, fontweight='bold')
    plt.ylabel('Height (µm)', fontsize=15, fontweight='bold')
    for index, dataframe in enumerate(dataframes):
        label_name = re.sub(r'OA.*', 'OA', dataframe[1]) + ' (PAO4)'
        if index == 0:
            if '10N' in dataframe[1]:
                plt.plot(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'], '--', color = 'black', linewidth=3, label=label_name)
            elif '20N' in dataframe[1]:
                plt.plot(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'], color = 'black', linewidth=3, label=label_name)
        else:
            if '10N' in dataframe[1]:
                plt.plot(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'], '--', linewidth=3, label=label_name)
            elif '20N' in dataframe[1]:
                plt.plot(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'], linewidth=3, label=label_name)

    graph_name = graph_name.replace('/', '')

    plt.legend(loc='upper right', prop={'weight': 'bold', 'size': 12}, frameon=False)
    # plt.savefig(f'{new_path}\\{graph_name}')
    plt.show()

#--------------------------------------------------------------------------------------------------------------
def find_xintercept(x_series, y_series):
    x_intercepts_list = []
    zeros_list = []
    for i in range(len(y_series)-1):
        if y_series[i] * y_series[i+1] <= 0: # if the product between two y-values change sign then x axis is crossed
            x0 = x_series[i]
            x1 = x_series[i+1]
            y0 = y_series[i]
            y1 = y_series[i+1]
            if y_series[i] == y_series[i+1]:
                continue
            x_intercept = x_series[i] - y_series[i] * (x_series[i + 1] - x_series[i]) / (y_series[i + 1] - y_series[i])
            if x_series[i] <= x_intercept <= x_series[i+1] and x_intercept not in x_intercepts_list:
                x_intercepts_list.append(x_intercept)
                zeros_list.append(0)
    return x_intercepts_list, zeros_list

#--------------------------------------------------------------------------------------------------------------
def area_integral(dataframes:list, parameter:str): # TODO fix logic error
    #length = 0.86mm # ask vinay <-- maybe use formula in Edwin's thesis
    intArea = {}
    grouped_bar_indices = []
    grouped_bar_dict = {}

    for index, dataframe in enumerate(dataframes):
        x_intercepts_list, zeros_list = find_xintercept(dataframe[0]['Distance (µm)'], dataframe[0]['Height (µm)'])
        x_intercepts_df = pd.DataFrame({'Distance (µm)':x_intercepts_list, 'Height (µm)': zeros_list})
        bump_area_df = pd.concat([(dataframe[0][dataframe[0]['Height (µm)'] > 0]), x_intercepts_df]).sort_values(by='Distance (µm)')
        hole_area_df = pd.concat([(dataframe[0][dataframe[0]['Height (µm)'] < 0]), x_intercepts_df]).sort_values(by='Distance (µm)')
        
        # print(bump_area_df.to_string()) # for testing
        # print(hole_area_df.to_string()) # for testing

        sanitized_name = re.sub(r'OA.*', 'OA', dataframe[1]) + ' (PAO4)'

        intArea[sanitized_name] = [intg.trapezoid(bump_area_df['Height (µm)'], bump_area_df['Distance (µm)']), abs(intg.trapezoid(hole_area_df['Height (µm)'], hole_area_df['Distance (µm)']))]
        if sanitized_name not in grouped_bar_indices:
            grouped_bar_indices.append(sanitized_name)
        if index == 0:
            grouped_bar_dict[parameter] = [abs(intg.trapezoid(hole_area_df['Height (µm)'], hole_area_df['Distance (µm)']))]
        else:
            grouped_bar_dict[parameter].extend([abs(intg.trapezoid(hole_area_df['Height (µm)'], hole_area_df['Distance (µm)']))])

    intArea = pd.DataFrame(intArea)
    intVolume = intArea * 860 # 860 micrometers is the length from optical profilometry settings
    intArea.index = ['Bump Area (µm squared)','Hole Area (µm squared)']
    intVolume.index = ['Bump Volume (µm cubed)','Hole Volume (µm cubed)']
    return [intArea.to_string(), intVolume.to_string(), grouped_bar_dict, grouped_bar_indices]
#fix or use formula in Edwin's thesis

#----------------------------------------------------------------------------------------

    # create reference bar where all the graphs will dip down from
    # find points where slope between two pts are relatively low on edges <-- ignore points where slope is low b/w these points
    #--- go from left to right and then from right to left <-- should create a variable called slope sensitivity <-- determines how many pts included
    # averages the y values out for all these points and set that as reference for each graph
    # Use each reference to add or subtract values so that all of them are somewhat all on the same reference & can be differentiated

if __name__ =='__main__':
    main()

    # <-- do regression for left and right sides, thicker lines, 
    # better scaling for x and y axes, 
    # aluminum