#This is an example of a code I used for my transiting exoplanets project. This code rebins datapoints on a light curve and propagates errors accordingly.
# This script takes the output from the run_pynapple.py script (the two json files), and generates statistical errors.
# Then it rebins all the data (intensities, errors, times, etc.) into bins of five datapoints.
# Finally, it saves these new data in json files starting with the name 'rebin'.


import matplotlib.pyplot as plt
import numpy as np
import json
import datetime
import dateutil
import matplotlib.dates as mdates
import pandas as pd

timestamp_file = './phototimestamps.json'			#can change to any named input file. This will be the x (time) axis
photoresults_file = './photoresults.json'			#can change to any named input file. This will be the y (intensity) axis

with open(timestamp_file) as time_file:    
	timestrings = json.load(time_file)

times = [dateutil.parser.parse(timestring) for timestring in timestrings]

with open(photoresults_file) as photo_file:    
	intensities = json.load(photo_file)

baseline_data = intensities[:59] + intensities[302:]	#creates a new list from two slices of an old list. These slices are the photometry before and after transit.
#print len(baseline_data)								#just a sanity check to see that baseline_data has the amount of points we expect

norm = 1 / (np.mean(baseline_data))


baseline_times = times[:59] + times[302:]
norm_intensities = np.array(intensities)*norm 			#brings our intensities up to 1
norm_baseline = np.array(baseline_data)*norm #takes the same data points as baseline_data, but these are normalized
residuals = norm_baseline-1
baseline_times = times[:59] + times[302:]		#cant just plot norm baseline vs times, as times is a much longer array. Need to slice as well...
fractional_error = np.std(residuals)
numerical_error = np.array(norm_intensities)*fractional_error


rebin_intensities = []
rebin_errors = []
rebin_timestamps = []
rebin_time_errors = []
n = 5								#number of datapoints per bin. As written, this can't currently be changed. Maybe later
i = 0								#dummy variable for loop
j = len(norm_intensities)/n 		#number of times loop should run

while i < j:
	new_intensity = (norm_intensities[n*i]+norm_intensities[(n*i)+1]+norm_intensities[(n*i)+2]+norm_intensities[(n*i)+3]+norm_intensities[(n*i)+4])/n
	rebin_intensities.append(new_intensity)
	#above terms sum the data points and divide by n, then append into the rebin_intensities array

	new_error = (((numerical_error[n*i]**2)+(numerical_error[(n*i)+1]**2)+(numerical_error[(n*i)+2]**2)+(numerical_error[(n*i)+3]**2)+(numerical_error[(n*i)+4]**2))**0.5)/n
	rebin_errors.append(new_error)
	#above terms add errors in quadrature then divide by n, then append into the rebin_intensities array

	new_timestamp = times[n*i]+((times[(n*i)+4]-times[n*i])/2)
	rebin_timestamps.append(str(new_timestamp))
	#sets the new time to be the old time plus half the difference in first and last times in the array. Currently does not add 10 secs for last exposure
	#saves data as a string for json

	new_time_error = ((times[(n*i)+4]-times[n*i])/2)
	rebin_time_errors.append(new_time_error.total_seconds())

	i = i+1

print len(rebin_intensities)
print len(rebin_errors)
print len(rebin_timestamps)
print len(rebin_time_errors)

with open('rebin_intensities.json', 'w') as out_json:
            json.dump( rebin_intensities, out_json, indent=2 )
with open('rebin_errors.json', 'w') as out_json:
            json.dump( rebin_errors, out_json, indent=2 )
with open('rebin_timestamps.json', 'w') as out_json:
            json.dump( rebin_timestamps, out_json, indent=2 )
with open('rebin_time_errors.json', 'w') as out_json:
            json.dump( rebin_time_errors, out_json, indent=2 )

