import time;

from pyindi import * 
pi = PyINDI(verbose=False)

#pi.setINDI("LMIRCAM.enable_save.value=On")    # Turn save on. Works.
#pi.setINDI("LMIRCAM.enable_save.value=On")    # Turn save on again, does it make problems if it is on already? No.
#pi.setINDI("LMIRCAM.enable_save.value=Off")   # Turn save off. Works.
#pi.setINDI("LMIRCAM.enable_save.value=Off")   # Turn save off again, does it make problems if it is on already? No.

# change to slow mode for long exposures
# pi.setINDI("LMIRCAM.enable_fast_mode.value=Off", timeout=30);
# pi.setINDI("LMIRCAM.acquire.int_time=54.9;num_coadds=1;num_seqs=1;enable_bg=0;is_bg=0;is_cont=0");

#pi.setINDI("LMIRCAM.acquire.int_time=0.0;num_coadds=1;num_seqs=1;enable_bg=0;is_bg=0;is_cont=1")      # Set camera in continuous.  Not working:  Not taking any frames, times out.

#time.sleep(5);	# let it run a short while

pi.setINDI("LMIRCAM.stop.value=Off")           #  Stop camera.  Not working:  Stops camera (and returns no error if camera not running), but returns timeout.
