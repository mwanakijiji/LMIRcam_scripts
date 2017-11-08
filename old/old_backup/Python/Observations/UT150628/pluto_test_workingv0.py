#!/usr/bin/python
#Darks/flats/linearity script
#AS-131019
#DD-150206-added datatype and wait statements
#AS-15001-corrected data types
#ES-150628-modified for more filters, specific to Pluto observation

#prereq: LMIR FW1 is LargeDualAperture


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
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True) # 'home' is the same as 'Open'
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "H2O-Ice2", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=DRK;Comment=SCI/CAL/DRK/FLT") # for inserting comment into FITS header

#save frames
# the below line means, 'set 1 coadd, and a sequence of 10 frames'
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_h2oice2), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)
    
################################
# L-CONT1

#set filters and datatype to L-CONT1
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "Lcont1", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_lcont1), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# N3309

#set filters and datatype to N3309
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "N03309-8", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_n3309), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# L-CONT2

#set filters and datatype to L-CONT2
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont2", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_lcont2), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# L-CONT3

#set filters and datatype to L-CONT3
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "Lcont3", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_lcont3), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# L-CONT4

#set filters and datatype to L-CONT4
pi.setINDI("Lmir.LMIR_FW2.command", "L-cont4", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "_home_", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_lcont4), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################
# BRA-ON

#set filters and datatype to BRA-ON
pi.setINDI("Lmir.LMIR_FW2.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW3.command", "_home_", timeout=20, wait=True)
pi.setINDI("Lmir.LMIR_FW4.command", "Br-Alpha-On", timeout=20, wait=True)
#pi.setINDI("LMIRCAM.EditFITS.Keyword=FLAG;Value=FLT;Comment=SCI/CAL/DRK/FLT")

#save frames
pi.setINDI("LMIRCAM.Command.text", "%f 1 2 lbtintpar 500 sleep" % (dit_braon), timeout=300)
pi.setINDI("LMIRCAM.Command.text", "go", timeout=300, wait=True)

################################

#turn off save data
pi.setINDI("LMIRCAM.Command.text", "0 savedata 1 autodispwhat 1 loglevel", wait=True)
