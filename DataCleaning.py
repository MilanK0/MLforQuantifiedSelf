""""
Ward van Rooij
Data Cleaning
"""


#Import necessities.
import pandas as pd
import scipy.stats as sstats
import numpy as np
from pykalman import KalmanFilter


lst =  ['timestamp', 'label:LYING_DOWN', 'label:SITTING', 'label:FIX_walking', 
       'label:FIX_running', 'label:OR_standing', 'label:BICYCLING',
       'raw_acc:3d:mean_x', 'raw_acc:3d:mean_y','raw_acc:3d:mean_z',
       'proc_gyro:3d:mean_x', 'proc_gyro:3d:mean_y', 'proc_gyro:3d:mean_z',
       'raw_magnet:3d:mean_x', 'raw_magnet:3d:mean_y', 'raw_magnet:3d:mean_z',
       'watch_acceleration:3d:mean_x', 'watch_acceleration:3d:mean_y', 'watch_acceleration:3d:mean_z',
       'location_quick_features:lat_change','location_quick_features:long_change',
       'location:min_speed','location:max_speed','audio_properties:max_abs_value','discrete:battery_state:is_charging',
       'discrete:ringer_mode:is_silent_no_vibrate','discrete:ringer_mode:is_silent_with_vibrate','discrete:ringer_mode:is_normal',
       'discrete:ringer_mode:missing','discrete:on_the_phone:is_True','discrete:on_the_phone:is_False',
       'discrete:on_the_phone:missing','lf_measurements:pressure','lf_measurements:proximity',
       'lf_measurements:temperature_ambient','lf_measurements:relative_humidity']
      

#Read file.
def read_file(file_name):
    base_dir = './datasets/'
    return pd.read_csv(base_dir + file_name + '.csv', usecols=lst)
    
def test():
    return 'hoi'


#Removing outliers based on threshold and replace them by nan.
def nan_outliers_value(data, value):
    
    #For multiple columns.
    if len(data.shape) > 1:
        for i in list(data.columns.values):
            outliers = (data[i] > value)
            data[i] = data[i].mask(outliers, np.nan)
    
    #For a single column.            
    else:
        outliers = (abs(data) > value)
        data = data.mask(outliers, np.nan)
            
    return data


#Removing outliers based on threshold of n standard deviations and replace
#them by nan.  
def nan_outliers_distribution(data, n_std):
    
    #For multiple columns.
    if len(data.shape) > 1:
        for i in list(data.columns.values):
            if sstats.mstats.normaltest(data[i])[1] < 0.05:
                print 'ERROR: One of the passed columns is not normally distributed.'
                return
            std_dev = data[i].std()
            mean = data[i].mean()
            outliers_min = (data[i] > (mean + n_std * std_dev))
            outliers_plus = (data[i] < (mean - n_std * std_dev))
            data[i] = data[i].mask(outliers_min, np.nan)
            data[i] = data[i].mask(outliers_plus, np.nan)
    
    #For a single column.            
    else:
        if sstats.mstats.normaltest(data)[1] < 0.05:
            print 'ERROR: The passed column is not normally distributed.'
            return
        std_dev = data.std()
        mean = data.mean()
        outliers_min = (data > (mean + n_std * std_dev))
        outliers_plus = (data < (mean - n_std * std_dev))
        data = data.mask(outliers_min, np.nan)
        data = data.mask(outliers_plus, np.nan)
        
    return data
    
    
#Removing outliers based on threshold and replace them by mean, median
#or interpolation.    
def replace_outliers_value(data, value, replacement_type, replacement_value=0):
    
    #For multiple columns.
    if len(data.shape) > 1:
        for i in list(data.columns.values):
            outliers = (data[i] > value)
            data[i] = data[i].mask(outliers, np.nan)
            if replacement_type == 'value':
                data[i] = data[i].fillna(replacement_value)
            if replacement_type == 'mean':
                data[i] = data[i].fillna(data[i].mean())
            if replacement_type == 'median':
                data[i] = data[i].fillna(data[i].median())
            if replacement_type == 'interpolate':
                data[i] = data[i].interpolate()
    
    #For a single column.            
    else:
        outliers = (abs(data) > value)
        data = data.mask(outliers, np.nan)
        if replacement_type == 'value':
            data = data.fillna(replacement_value)
        if replacement_type == 'mean':
            data = data.fillna(data.mean())
        if replacement_type == 'median':
            data = data.fillna(data.median())
        if replacement_type == 'interpolate':
            data = data.interpolate()
            
    return data

    
#Removing outliers based on threshold of n standard deviations and replace
#them by mean, median or interpolation.    
def replace_outliers_distribution(data, n_std, replacement_type, replacement_value=0):
    
    #For multiple columns.
    if len(data.shape) > 1:
        for i in list(data.columns.values):
            if sstats.mstats.normaltest(data[i])[1] < 0.05:
                print 'ERROR: One of the passed columns is not normally distributed.'
                return
            std_dev = data[i].std()
            mean = data[i].mean()
            outliers_min = (data[i] > (mean + n_std * std_dev))
            outliers_plus = (data[i] < (mean - n_std * std_dev))
            data[i] = data[i].mask(outliers_min, np.nan)
            data[i] = data[i].mask(outliers_plus, np.nan)
            if replacement_type == 'value':
                data[i] = data[i].fillna(replacement_value)
            if replacement_type == 'mean':
                data[i] = data[i].fillna(data[i].mean())
            if replacement_type == 'median':
                data[i] = data[i].fillna(data[i].median())
            if replacement_type == 'interpolate':
                data[i] = data[i].interpolate()
    
    #For a single column.            
    else:
        if sstats.mstats.normaltest(data)[1] < 0.05:
            print 'ERROR: The passed column is not normally distributed.'
            return
        std_dev = data.std()
        mean = data.mean()
        outliers_min = (data > (mean + n_std * std_dev))
        outliers_plus = (data < (mean - n_std * std_dev))
        data = data.mask(outliers_min, np.nan)
        data = data.mask(outliers_plus, np.nan)
        if replacement_type == 'value':
            data = data.fillna(replacement_value)
        if replacement_type == 'mean':
            data = data.fillna(data.mean())
        if replacement_type == 'median':
            data = data.fillna(data.median())
        if replacement_type == 'interpolate':
            data = data.interpolate()
            
    return data
    

#Impute missing values.
def impute_missing(data, filler_type, replacement_value=0):
    
    #For multiple columns.
    if len(data.shape) > 1:
        for i in list(data.columns.values):
            if filler_type == 'value':
                data[i] = data[i].fillna(replacement_value)
            if filler_type == 'mean':
                data[i] = data[i].fillna(data[i].mean())
            if filler_type == 'median':
                data[i] = data[i].fillna(data[i].median())
            if filler_type == 'interpolate':
                data[i] = data[i].interpolate()
    
    #For a single column.
    else:
        if filler_type == 'value':
            data = data.fillna(replacement_value)
        if filler_type == 'mean':
            data = data.fillna(data.mean())
        if filler_type == 'median':
            data = data.fillna(data.median())
        if filler_type == 'interpolate':
            data = data.interpolate()
            
    return data


#Rename columns.
def rename_columns(data, lst):
    result = pd.DataFrame()
    for i in list(data.columns.values):
        result[lst[list(data.columns.values).index(i)]] = data[i]
    return result


#Report percentage of missing values per attribute.
def percentage_missing_values(data):
    result = []
    for i in list(data.columns.values):
        row = []
        missing = (float(len(data[i])) - float(data[i].count())) / float(len(data[i]))
        row.append(i)
        row.append(missing)
        result.append(row)
    return pd.DataFrame(result)
      

#Applying a Kalman filter.
def kalman_filter(data, col):

    # Initialize the Kalman filter with the trivial transition and observation matrices.
    kf = KalmanFilter(transition_matrices = [[1]], observation_matrices = [[1]])

    numpy_array_state = data.as_matrix(columns=[col])
    numpy_array_state = numpy_array_state.astype(np.float32)
    numpy_matrix_state_with_mask = np.ma.masked_invalid(numpy_array_state)

    # Find the best other parameters based on the data (e.g. Q)
    kf = kf.em(numpy_matrix_state_with_mask, n_iter=5)

    # And apply the filter.
    (new_data, filtered_state_covariances) = kf.filter(numpy_matrix_state_with_mask)

    data[col + '_kalman'] = new_data
    return data
    
    