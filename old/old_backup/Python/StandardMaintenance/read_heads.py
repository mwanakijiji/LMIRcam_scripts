import pyfits
import numpy
#import matplotlib
#import pylab
#from pylab import *

base = 'lm_150208_'
abcissa = []
expTimeOrdinate = []
data = []
for x in range(31500,33318):
	hdu = pyfits.open(base+str(x)+'.fits')
	head = hdu[0].header
	print x
	print head['EXPTIME']
	expTime = float(head['EXPTIME'])
	print head['LMIR_FW1']
	print head['LMIR_FW2']
	print head['LMIR_FW3']
	print head['LMIR_FW4']
	print '----'
	hdu.close()
	#abcissa.append(x)
	#expTimeOrdinate.append(expTime)
	data.append([x,expTime])
numpy.savetxt('exptimes',numpy.array(data))
#plot(abcissa,expTimeOrdinate)
#show()
