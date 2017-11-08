import pyfits
import numpy
#import matplotlib
#import pylab
#from pylab import *

base = 'lm_150626_' # filename with UT date
abcissa = []
expTimeOrdinate = []
data = []
medianArray = []
xrange = range(507,517) # a central box on the array
yrange = xrange
medianArray10FramesTogether = []
numberOfFramesTotal = 160 # frames that had been written out by linearity script
interval = 10 # number of frames spit out for each combination of parameters, to be averaged
startFrame = 4467 # starting frame (probably a dark)

for y in range(0,numberOfFramesTotal):
	medianArray10FramesSeparate = []
	for x in range(startFrame+interval*y,startFrame+interval*y+interval): 			
		dataArray = pyfits.getdata(base+"%05d" % (startFrame)+'.fits',0)
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
