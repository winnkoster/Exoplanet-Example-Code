#This is an example of a code I used for my transiting exoplanets project. This code makes pretty plots of my data!

import matplotlib.pyplot as plt
import numpy as np
import json
import datetime
import dateutil
import matplotlib.dates as mdates
import pandas as pd

timestamp_file = './rebin_timestamps.json'
photoresults_file = './rebin_intensities.json'
time_errors_file = './rebin_time_errors.json'
photo_errors_file = './rebin_errors.json'


with open(timestamp_file) as time_file:    
	timestrings = json.load(time_file)

times = [dateutil.parser.parse(timestring) for timestring in timestrings]

with open(photoresults_file) as photo_file:    
	intensities = json.load(photo_file)

with open(time_errors_file) as time_error_file:
	time_errors_floats = json.load(time_error_file)

time_errors = [datetime.timedelta(seconds=time_float) for time_float in time_errors_floats] 

with open(photo_errors_file) as photo_error_file:
	intensities_errors = json.load(photo_error_file)

hfmt = mdates.DateFormatter('%m-%d %H:%M') 

f = plt.figure()
plt.errorbar(times, intensities, xerr=time_errors, yerr=intensities_errors, marker='.', linestyle='None')
plt.title('Transit of Wasp 23b, November 15, 2015')
plt.axhline(y=1, xmin=0, xmax=1, linewidth=1, color = 'k')	#plots a line across y=1

ax = plt.gca()

# end_trans = pd.to_datetime('2016-11-19 21:51:00')
# text_marker1 = pd.to_datetime('2016-11-19 20:20:00')
# text_marker2 = pd.to_datetime('2016-11-19 21:34:30')
# text_marker3 = pd.to_datetime('2016-11-19 21:51:30')
# ax.axvline(end_trans, color='r', lw=1)

#ax.annotate('End Transit', xy=(end_trans,1), xytext=(text_marker2,1.10), color='r')
#ax.annotate('21:51', xy=(end_trans,1), xytext=(text_marker3,0.965), color='r')
#ax.annotate('Transit begins before plot at 20:10', xy=(end_trans,1), xytext=(text_marker1,1.10), color='g')

# Get current axis 
# Apply formatter to the x-axis of the current axis.
ax.xaxis.set_major_formatter(hfmt)
# Optional - Place ticks every 15 mins, etc.
ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute = [30]))
plt.ylabel('Intensity (arbitrary units)')

f.savefig("foo.pdf")
plt.show()