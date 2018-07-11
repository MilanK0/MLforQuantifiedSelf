# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:28:17 2018

@author: milan
"""

import DataCleaning as dc
import DataExploration as de
import matplotlib.pyplot as plt

data = dc.read_file('final_assignment') 

print data.shape
print data.columns.values

#Drop elke kolom met niks dan missing values.
data = data.dropna(axis=1, how='all')
print data.shape

#Dan blijven deze dus over
print data.columns.values

import pandas as pd
pd.set_option('display.max_columns', 50)

descriptives = data.describe()

lst = []
for i in list(data.columns.values):
    b = []
    a = (float(len(data[i])) - float(data[i].count())) / float(len(data[i]))
    b.append(i)
    b.append(a)
    lst.append(b)
    
#Percentages missing value per attribute
import numpy as np
lst = pd.DataFrame(lst)
print lst

#Watch acceleration origineel
plt.scatter(range(len(data['watch_acceleration:3d:mean_x'])), data['watch_acceleration:3d:mean_x'], s=1)
plt.show()

#Watch acceleration Kalman
plt.scatter(range(len(data['watch_acceleration:3d:mean_x_kalman'])), data['watch_acceleration:3d:mean_x_kalman'], s=1)
plt.show()

plt.scatter(range(len(data['raw_acc:3d:mean_x'])), data['raw_acc:3d:mean_x'], s=1)
plt.show()

#Watch acceleration interpolate
plt.scatter(range(len(data_watch_acc['watch_acceleration:3d:mean_x'])), data_watch_acc['watch_acceleration:3d:mean_x'], s=1)
plt.show()

#Extra variabelen maken met of waar missing data zit.
data['missing_watch_acc_x'] = pd.isnull(data_watch_acc['watch_acceleration:3d:mean_x']).astype(int)
data['missing_watch_acc_x'] = pd.isnull(data_watch_acc['watch_acceleration:3d:mean_y']).astype(int)
data['missing_watch_acc_x'] = pd.isnull(data_watch_acc['watch_acceleration:3d:mean_z']).astype(int)

plt.scatter(range(len(data['location:min_speed'])), data['location:min_speed'], s=1)
plt.show()

plt.scatter(range(len(data['location:min_speed'])), data['location:min_speed'], s=1)
plt.show()

data = dc.kalman_filter(data, 'watch_acceleration:3d:mean_x')

data_raw_magnet = dc.impute_missing(data[['raw_magnet:3d:mean_x','raw_magnet:3d:mean_y','raw_magnet:3d:mean_z']], 'interpolate')

#Extra variabelen maken met of waar missing data zit.
data['missing_location:min_speed'] = pd.isnull(data['location:min_speed']).astype(int)
data['missing_location:max_speed'] = pd.isnull(data['location:max_speed']).astype(int)

data.describe()
data_watch_acc.describe()

plt.scatter(range(len(data['audio_properties:max_abs_value'])), data['audio_properties:max_abs_value'], s=1)
plt.show()

data_audio_interp = dc.impute_missing(data['audio_properties:max_abs_value'], 'value', replacement_value=0.5)
plt.scatter(range(len(data_audio_interp)), data_audio_interp, s=1)
plt.show()

plt.scatter(range(len(data['location:max_speed'])), data['location:max_speed'], s=1)
plt.show()

plt.plot(range(len(lst[:,1])), lst[:,1])
plt.show()

data.rename(columns={"raw_acc:3d:mean_x": "acc_x", "raw_acc:3d:mean_y": "acc_y"})
print data.columns.values

data['raw_acc:3d:mean_x'].describe()
print dc.rename_columns(data[['raw_acc:3d:mean_x', 'raw_acc:3d:mean_y', 'raw_acc:3d:mean_z']], ['acc_x', 'acc_y', 'acc_z'])