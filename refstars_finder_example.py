#This is an example of a code I used for my transiting exoplanets project. This code helped me find reference stars for Wasp 23b.
#This is a variant of the standard pynapple code that simply writes the flux counts of reference stars to a file, to be plotted later,
#as opposed to comparing the flux counts from several sources to generate a normalized, controled light curve)

import pynapple as pyn
import os
from astropy import units as u
import astropy.io.fits as pyfits
import numpy as np
import json

#defining reference stars and target
wasp23 = pyn.pynStar('06:44:30.608', '-42:45:44.02', unit=(u.hour, u.deg))
refA = pyn.pynStar('06:44:41.2','-42:43:50.9', unit=(u.hour, u.deg))
refB = pyn.pynStar('06:44:45.4','-42:42:08.0', unit=(u.hour, u.deg))
refC = pyn.pynStar('06:44:28.2','-42:47:07.8', unit=(u.hour, u.deg))
refD = pyn.pynStar('06:44:45.6','-42:47:34.4', unit=(u.hour, u.deg))
refE = pyn.pynStar('06:44:28.2','-42:43:56.9', unit=(u.hour, u.deg))
refF = pyn.pynStar('06:44:22.1','-42:43:20.5', unit=(u.hour, u.deg))
refG = pyn.pynStar('06:44:27.2','-42:46:23.3', unit=(u.hour, u.deg))
refH = pyn.pynStar('06:44:35.6','-42:46:28.0', unit=(u.hour, u.deg))

mystars = [wasp23, refA, refB, refC, refD, refE, refF, refG, refH]

inputfolder = './ReducedData'
files = [os.path.join(inputfolder, filename) for filename in \
	os.listdir(inputfolder) if filename.endswith('.fits')]
files.sort()

wasp23_counts = []
refA_counts = []
refB_counts = []
refC_counts = []
refD_counts = []
refE_counts = []
refF_counts = []
refG_counts = []
refH_counts = []
timestamps = []


for index, path in enumerate(files):
		filename = os.path.split(path)[1]
		print 'Analysing %s of %s: %s' % (index+1, len(files), filename)

		myfits = pyfits.open(path)
		myimage = pyn.pynImage(myfits)
		image_timestamp = str(myimage.centretime)		#pulls the time of exposure as a string from the fits header and saves it as 'time'

		photodata = pyn.doPhotometry(myimage, mystars)
		signal, noise = pyn.calcHowellErrors(photodata, myimage.exptime)

		snr = signal / noise

		#print np.max(snr[:,0])			#prints the SNR for the various aperture settings, selecting ONLY the MAX of target star column
		#print np.argmax(snr[:,0])		#prints which aperture setting the max comes from

		best_snr = np.argmax(snr[:,0])

		#print signal[best_snr,:]		#prints signal counts fron the highest SNR for all four stars
		signal_counts = signal[best_snr,:]
		noise_counts = noise[best_snr,:]

		target_signal = signal_counts[0]
		refA_signal = signal_counts[1]
		refB_signal = signal_counts[2]
		refC_signal = signal_counts[3]
		refD_signal = signal_counts[4]
		refE_signal = signal_counts[5]
		refF_signal = signal_counts[6]
		refG_signal = signal_counts[7]
		refH_signal = signal_counts[8]

		wasp23_counts.append(target_signal)
		refA_counts.append(refA_signal)
		refB_counts.append(refB_signal)
		refC_counts.append(refC_signal)
		refD_counts.append(refD_signal)
		refE_counts.append(refE_signal)
		refF_counts.append(refF_signal)
		refG_counts.append(refG_signal)
		refH_counts.append(refH_signal)
		
		timestamps.append(image_timestamp)
		


with open('wasp23_counts.json', 'w') as out_json:
            json.dump( wasp23_counts, out_json, indent=2 )
with open('refA_counts.json', 'w') as out_json:
            json.dump( refA_counts, out_json, indent=2 )
with open('refB_counts.json', 'w') as out_json:
            json.dump( refB_counts, out_json, indent=2 )
with open('refC_counts.json', 'w') as out_json:
            json.dump( refC_counts, out_json, indent=2 )
with open('refD_counts.json', 'w') as out_json:
            json.dump( refD_counts, out_json, indent=2 )
with open('refE_counts.json', 'w') as out_json:
            json.dump( refE_counts, out_json, indent=2 )
with open('refF_counts.json', 'w') as out_json:
            json.dump( refF_counts, out_json, indent=2 )
with open('refG_counts.json', 'w') as out_json:
            json.dump( refG_counts, out_json, indent=2 )        
with open('refH_counts.json', 'w') as out_json:
            json.dump( refH_counts, out_json, indent=2 )
with open('phototimestamps.json', 'w') as out_json:
            json.dump( timestamps, out_json, indent=2 )





