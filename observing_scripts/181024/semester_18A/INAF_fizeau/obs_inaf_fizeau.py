from lmircam_tools import pi
from lmircam_tools.align_spec import align_spec
from lmircam_tools.track_fizeau import track_spectral_fringes as track
from lmircam_tools.exposures import get_lmircam_frames
from lmircam_tools.utils import nod, rawbg, setFLAG
from lmircam_tools.print_tools import *
from multiprocessing import Process
from time import sleep

#################################################
# USER DEFINED PARAMETERS                       #
#################################################

# camera
dit = 0.0            # DIT. 0.0 for minimum, should be standard.
ndit_fringes = 20   # Number of integrations per nod on fringes.
ndit_spec = 10       # Number of integrations per nod on not overlapped spectra.
coadds = 1           # Do not change!
nnods_fringes = 1    # Number of nod pairs on fringes.
savedata = True      # Save data? Can be 'True' or 'False'.
inner_loop_max = 10  # Maximum number of frames taken at once.
track_fringes = False # Track fringes? Can be True' or 'False'. Not working yet, so leave False.
sleep_cont = 2.0     # Extra sleep time after stopping continuous acquisition (s).

# telesecope
nod_x = 1.45         # arcseconds in detector coords
i_nods_done = 0      # number of nods finished (see Instructions above on how to use)

# bands
do_lband = True      # take L band data? (True/False)
do_mband = True      # take N band data? (True/False)

#################################################
# COMPUTATIONS/DEFINITIONS                      #
#################################################

nod_names = ['LEFT','RIGHT']

#################################################
# COMMAND SEQUENCE                              #
#################################################

print ''
request('Please set up for observations:')
print '  Field of view: "FIZEAU_spec_L", (for both L OR M band!)'
print '  Grism "Lgrism6AR", filter "Janos3.0-5.0" (for both L OR M band!)'
print '  L band (top long part, for both L OR M band!) of Spectra vertically centered'
print '  and approx. horizontally overlapped on column ~195,'
print '  Fringes approx. upright.'
print '  Hit [RETURN] when done.'; raw_input()



if do_lband:

# Take fringe data in left nod position in L band.
  
  nod_pos='LEFT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  print ''
  info('Aligning spectra.')
  align_spec(nod_pos = nod_pos)
  
  print ''
  request('Please check alignment of spectra, adjust if needed.')
  print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  if track_fringes:
    track = Process(target=track, args=(nod_pos, 'lband'))
    track.start()
    sleep(0.3)
  else:
    request('Make sure fringes are vertical.')
    print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  info('Integrating: L band fringes, left nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=fringes;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_fringes, inner_loop_max = inner_loop_max)
  
  if track_fringes:
    track.terminate()
  
# Nod right
  
  print ''
  info('Nodding right.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata', wait=True)
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(nod_x, 0, 'both')



# Take fringe data in right nod position in L band.
  
  nod_pos='RIGHT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  print ''
  info('Aligning spectra.')
  align_spec(nod_pos = nod_pos)
  
  print ''
  request('Please check alignment of spectra, adjust if needed.')
  print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  if track_fringes:
    track = Process(target=track, args=(nod_pos, 'lband'))
    track.start()
    sleep(0.3)
  else:
    request('Make sure fringes are vertical.')
    print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  info('Integrating: L band fringes, right nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=fringes;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_fringes, inner_loop_max = inner_loop_max)
  
  if track_fringes:
    track.terminate()
  
# Nod left
  
  print ''
  info('Nodding left.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(-nod_x, 0, 'both')



if do_mband:

# Take fringe data in left nod position in M band.
  
  nod_pos='LEFT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  pi.setINDI('LMIRCAM.Command.text', '0 contacq')
  sleep(sleep_cont)
  pi.setINDI('LMIRCAM.Command.text=" FIZEAU_spec_M" subsectmap')
  
  print ''
  info('Aligning spectra.')
  align_spec(nod_pos = nod_pos)
  
  print ''
  request('Please check alignment of spectra, adjust if needed.')
  print '  Hit [RETURN] when done.'; raw_input()

  print ''
  if track_fringes:
    track = Process(target=track, args=(nod_pos, 'mband'))
    track.start()
    sleep(0.3)
  else:
    request('Make sure fringes are vertical.')
    print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  info('Integrating: M band fringes, left nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=fringes;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_fringes, inner_loop_max = inner_loop_max)
  
  if track_fringes:
    track.terminate()
  
# Nod right
  
  print ''
  info('Nodding right.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(nod_x, 0, 'both')



# Take fringe data in right nod position in M band.
  
  nod_pos='RIGHT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  print ''
  info('Aligning spectra.')
  align_spec(nod_pos = nod_pos)
  
  print ''
  request('Please check alignment of spectra, adjust if needed.')
  print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  if track_fringes:
    track = Process(target=track, args=(nod_pos, 'mband'))
    track.start()
    sleep(0.3)
  else:
    request('Make sure fringes are vertical.')
    print '  Hit [RETURN] when done.'; raw_input()
  
  print ''
  info('Integrating: M band fringes, right nod position.')  
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=fringes;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_fringes, inner_loop_max = inner_loop_max)
  
  if track_fringes:
    track.terminate()
  
# Nod left
  
  print ''
  info('Nodding left.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(-nod_x, 0, 'both')

# Nod separate spectra (left side left)

print ''
info('Nodding left, separating spectra.')
pi.setINDI('LMIRCAM.Command.text', '0 savedata')
pi.setINDI('LMIRCAM.Command.text', '0 contacq')
sleep(sleep_cont)
pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
sleep(0.3)
pi.setINDI('LMIRCAM.Command.text', '1 contacq')
nod(-1.0 * nod_x, 0, 'left')



if do_lband:

# Take spectra data in left nod position in L band.
  
  nod_pos='LEFT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  pi.setINDI('LMIRCAM.Command.text', '0 contacq')
  sleep(sleep_cont)
  pi.setINDI('LMIRCAM.Command.text=" FIZEAU_spec_L" subsectmap')
  
  print ''
  info('Integrating: L band spectra, left nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=spectra;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  
  print ''
  info('Integrating: L band spectral calib, left nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=speccal;Comment=type of data obtained in fizeau mode.')
  pi.setINDI("Lmir.lmir_FW4.command", 'H2O-Ice2', timeout=45, wait=True)
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  pi.setINDI("Lmir.lmir_FW4.command", 'Br-Alpha-On', timeout=45, wait=True)
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  pi.setINDI("Lmir.lmir_FW4.command", 'Open', timeout=45, wait=True)
  
# Nod right
  
  print ''
  info('Nodding right.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(2.0 * nod_x, 0, 'both')
  
  
  
# Take spectra data in right nod position in L band.
  
  nod_pos='RIGHT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  print ''
  info('Integrating: L band spectra, right nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=spectra;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  
  print ''
  info('Integrating: L band spectral calib, right nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=speccal;Comment=type of data obtained in fizeau mode.')
  pi.setINDI("Lmir.lmir_FW4.command", 'H2O-Ice2', timeout=45, wait=True)
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  pi.setINDI("Lmir.lmir_FW4.command", 'Br-Alpha-On', timeout=45, wait=True)
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  pi.setINDI("Lmir.lmir_FW4.command", 'Open', timeout=45, wait=True)
  
  
  
# Nod left
  
  print ''
  info('Nodding left.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(-2.0 * nod_x, 0, 'both')



if do_mband:
  
# Take spectra data in left nod position in M band.
  
  nod_pos='LEFT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  pi.setINDI('LMIRCAM.Command.text', '0 contacq')
  sleep(sleep_cont)
  pi.setINDI('LMIRCAM.Command.text=" FIZEAU_spec_M" subsectmap')
  
  print ''
  info('Integrating: M band spectra, left nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=spectra;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  
  print ''
  info('Integrating: M band spectral calib, left nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=speccal;Comment=type of data obtained in fizeau mode.')
  pi.setINDI("Lmir.lmir_FW4.command", 'Std-M', timeout=45, wait=True)
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  pi.setINDI("Lmir.lmir_FW4.command", 'Open', timeout=45, wait=True)
  
  
  
# Nod right
  
  print ''
  info('Nodding right.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(2.0 * nod_x, 0, 'both')
  
  
  
# Take spectra data in right nod position in M band.
  
  nod_pos='RIGHT'     # nod_pos can be 'LEFT' or 'RIGHT'
  pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=' + nod_pos + ';Comment=nod position in fizeau mode.')
  
  print ''
  info('Integrating: M band spectra, right nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=spectra;Comment=type of data obtained in fizeau mode.')
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  
  
  print ''
  info('Integrating: M band spectral calib, right nod position.')
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=speccal;Comment=type of data obtained in fizeau mode.')
  pi.setINDI("Lmir.lmir_FW4.command", 'Std-M', timeout=45, wait=True)
  get_lmircam_frames(dit, coadds, ndit_spec, inner_loop_max = inner_loop_max)
  pi.setINDI("Lmir.lmir_FW4.command", 'Open', timeout=45, wait=True)


# Nod left
  
  print ''
  info('Nodding left.')
  pi.setINDI('LMIRCAM.Command.text', '0 savedata')
  pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
  sleep(0.3)
  pi.setINDI('LMIRCAM.Command.text', '1 contacq')
  nod(-2.0 * nod_x, 0, 'both')


# Reset nod position

print ''
info('Resetting nod positions.')
pi.setINDI('LMIRCAM.Command.text', '0 savedata')
pi.setINDI('LMIRCAM.Command.text', '0 contacq')
sleep(sleep_cont)
pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, 1, 1), wait=True)
sleep(0.3)
pi.setINDI('LMIRCAM.Command.text', '1 contacq')
nod(nod_x, 0, 'left')



# Reset camera

pi.setINDI('LMIRCAM.Command.text', '0 contacq')
pi.setINDI('LMIRCAM.Command.text', '0 contacq')
sleep(sleep_cont)
pi.setINDI('LMIRCAM.Command.text=" FIZEAU_spec_L" subsectmap')
pi.setINDI('LMIRCAM.Command.text', '0 savedata')
sleep(0.3)
pi.setINDI('LMIRCAM.Command.text', '1 contacq')



#Reset fits keywords

pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=N/A;Comment=type of data obtained in fizeau mode.')
pi.setINDI('LMIRCAM.EditFITS.Keyword=nodpos;Value=N/A;Comment=nod position in fizeau mode.')


request('Script finished. Please start new observation.')
