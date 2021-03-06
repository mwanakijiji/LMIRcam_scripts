#!/usr/bin/python

from lmircam_tools.overlap_psfs import overlap_airy_psfs



############## BEGIN GROSS OVERLAP OF AIRY PSFS

psf_loc_setpoint = [1220,800]  # pixel location for PSFs to be at
overlap_airy_psfs(psf_loc_setpoint)

############## END GROSS OVERLAP OF AIRY PSFS



############## BEGIN PUT IN GRISM AND REFINE GRISM-PSF OVERLAP

# don't know how separate the grism PSFs will be here...

############## END PUT IN GRISM AND REFINE GRISM-PSF OVERLAP


############## BEGIN DIAL OPD WITH HPC AND FIND CENTER OF COHERENCE ENVELOPE, THEN REMOVE GRISM

############## END DIAL OPD WITH HPC AND FIND CENTER OF COHERENCE ENVELOPE, THEN REMOVE GRISM


############## BEGIN HOLD CENTER OF SCIENCE COHERENCE ENVELOPE WITH HIGH-CONTRAST FRINGES

############## END HOLD CENTER OF SCIENCE COHERENCE ENVELOPE WITH HIGH-CONTRAST FRINGES


############## TRANSLATE NIL + CLOSE PHASECAM LOOP HERE?

############## OPTIMIZE SCIENCE PSF BY FINDING OPD AND TT SETPOINTS ITERATIVELY


############## SET FLAG IN SCIENCE IMAGE HEADERS TO EFFECT FIZEAU IS CONTROLLED

############## KEEP TRACK OF FRINGES IN SCIENCE READOUTS
