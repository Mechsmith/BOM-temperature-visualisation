"""This program displays a graph of the maximum temperatures at Perth
   Airport from 03 June 1944 to 01 June 2021"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

def dataframe(filename):
    """Converts the .csv file into a pandas dataframe"""
    data = pd.read_csv(filename)
    return data

    
def clean_nan(data, data_column):
    """Takes pandas dataframe of data and removes all rows containing NaN"""
    data.dropna(subset=[data_column, \
                        'Quality'], inplace=True)
    return data

#def general_clean(data):
    #"""Final cleaning of rows that are of unacceptable quality"""
    #data = data[data['Quality'].str.contains('N')==False]
    #return data

def get_times(data):
    """Takes date information from columns to make a timestamp column"""
    date_list = []
    
    
    year_list = list(data['Year'])
    month_list = list(data['Month'])
    day_list = list(data['Day'])
    
    for i in range(0, len(year_list)):
        date_list.append(str(year_list[i]) + '-' + str(month_list[i]) + '-' + \
                         str(day_list[i]))
    
    data['Date'] = date_list
    data['Date'] = pd.to_datetime(data['Date'])
    
    #Now add another date column, but as ordinals
    ordinal_list = []
    for date in date_list:
        d = dt.strptime(date, '%Y-%m-%d').date()
        ordinal_list.append(d)
    
    for i in range(len(ordinal_list)):
        ordinal_list[i] = ordinal_list[i].toordinal()
    data['Ordinal'] = ordinal_list

    return data
    

def data_vis(data, data_column):
    """Graphs data from the desired column versus time"""
    plt.figure(figsize=(15, 10))
    
    xtick_set = set(list(data['Year']))
    
    x_pts = list(data['Ordinal'])
    y_pts = list(data[data_column])
    
    regress = np.polyfit(list(data['Ordinal']), y_pts, 3)
    x_vals = np.linspace(list(data['Ordinal'])[0], list(data['Ordinal'])[-1], \
                         100000)
    y_vals = np.polyval(regress, x_vals)
    
    
    plt.plot(x_pts, y_pts)
    plt.plot(x_vals, y_vals, marker='.')
    plt.xticks(ticks=np.linspace(min(data['Ordinal']), \
                                 max(data['Ordinal']), \
                                 len(list(xtick_set))), \
               labels=list(xtick_set), rotation=90, fontsize=5)

    plt.show()

def main():
    filename = str(input("Name of data file: "))
    data = dataframe(filename)
    
    data_column = str(input("Name of column containing climate data: "))
    data = clean_nan(data, data_column)
    data = get_times(data)
    data_vis(data, data_column)
    