import pyfits
import numpy
#import matplotlib
#import pylab
#from pylab import *

base = 'lm_150208_'
abcissa = []
expTimeOrdinate = []
data = []
medianArray = []
xrange = range(507,517)
yrange = xrange
medianArray10FramesTogether = []

for y in range(0,160):
	medianArray10FramesSeparate = []
	for x in range(31718+10*y,31728+10*y):			
		dataArray = pyfits.getdata(base+str(x)+'.fits',0)
		lightMedian = numpy.median(dataArray[0,xrange,yrange])
		medianArray10FramesSeparate.append(lightMedian)
	medianArray10FramesTogether.append(numpy.mean(medianArray10FramesSeparate))
#print medianArray10FramesSeparate
#print medianArray10FramesTogether
numpy.savetxt('medianCentralVals',numpy.array(medianArray10FramesTogether))


	#hdu.close()
	
#numpy.savetxt('exptimes',numpy.array(data))
#plot(abcissa,expTimeOrdinate)
#show()

# old stuff that may be useful
	#head = hdu[0].header
	#print x
	#print head['EXPTIME']
	#expTime = float(head['EXPTIME'])
	#print head['LMIR_FW1']
	#print head['LMIR_FW2']
	#print head['LMIR_FW3']
	#print head['LMIR_FW4']
	#print '----'
	#abcissa.append(x)
	#expTimeOrdinate.append(expTime)
	#data.append([x,expTime])
