#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019
#DD-150206-added datatype and wait statements
#AS-15001-corrected data types
#ES-150628-modified for more filters, specific to Pluto observation

#


################################
# PARAMETERS TO BE SET BY USER 

# detector integration times (must be multiples of 0.029 sec)
dit_h2oice2 = 0.029
dit_lcont1 = 0.029
dit_n3309 = 0.029
dit_lcont2 = 0.029
dit_lcont3 = 0.029
dit_lcont4 = 0.029
dit_braon = 0.029

# number of coadds
coadd_h2oice2 = 1
coadd_lcont1 = 1
coadd_n3309 = 1
coadd_lcont2 = 1
coadd_lcont3 = 1
coadd_lcont4 = 1
coadd_braon = 1

# sequences per nod position
seq_h2oice2 = 1
seq_lcont1 = 1
seq_n3309 = 1
seq_lcont2 = 1
seq_lcont3 = 1
seq_lcont4 = 1
seq_braon = 1


# notes
# 1. prereq: LMIR FW1 is LargeDualAperture

# END PARAMETERS SET BY USER 
##############################


from pyindi import * 

#pi is an instance of PyINDI. Here we connect to the lmircam server
pi=PyINDI(verbose=True)

#turn on save data
pi.setINDI("LMIRCAM.Command.text", "1 savedata 0 autodispwhat 0 loglevel", wait=True)

################################
# H20 ICE2

#set and obstype filters to H2O ICE2
print 'Switching to H2O Ice2...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True) # 'home' is the same as 'Open'
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "H2O-Ice2", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT") # for inserting comment into FITS header

#save frames
# the below line means, 'set 1 coadd, and a sequence of 10 frames'
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_h2oice2, coadd_h2oice2, seq_h2oice2), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)


################################
# L-CONT1

#set filters and datatype to L-CONT1
print 'Switching to L-cont1...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "Lcont1", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont1, coadd_lcont1, seq_lcont1), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# N3309

#set filters and datatype to N3309
print 'Switching to N3309...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "N03309-8", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_n3309, coadd_n3309, seq_n3309), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# L-CONT2

#set filters and datatype to L-CONT2
print 'Switching to L-cont2...'
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont2, coadd_lcont2, seq_lcont2), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# L-CONT3

#set filters and datatype to L-CONT3
print 'Switching to L-cont3...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "Lcont3", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont3, coadd_lcont3, seq_lcont3), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# L-CONT4

#set filters and datatype to L-CONT4
print 'Switching to L-cont4...'
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_lcont4, coadd_lcont4, seq_lcont4), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# BRA-ON

#set filters and datatype to BRA-ON
print 'Switching to Bra-On...'
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "Br-Alpha-On", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f %d %d lbtintpar 500 sleep" % (dit_braon, coadd_braon, seq_braon), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 1 loglevel", wait=True)
