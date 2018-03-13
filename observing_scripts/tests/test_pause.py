from pyindi import *
from time import sleep 

pi = PyINDI(verbose=False)

side = 'right'   # chance to 'left', 'right', or 'both'

for i in range(0, 5):
  print 'Resuming AO.'
  if side == 'left' or side == 'both':
    pi.setINDI('ao_indi_sx_ice.resume.arg', '1', wait=True)
  if side == 'right' or side == 'both':
    pi.setINDI('ao_indi_dx_ice.resume.arg', '1', wait=True)
  sleep(5)
  print 'Pausing AO.'
  if side == 'left' or side == 'both':
    pi.setINDI('ao_indi_sx_ice.pause.arg', '1', wait=True)
  if side == 'right' or side == 'both':
    pi.setINDI('ao_indi_dx_ice.pause.arg', '1', wait=True)
  sleep(5)

print 'Resuming AO.'
if side == 'left' or side == 'both':
  pi.setINDI('ao_indi_sx_ice.resume.arg', '1', wait=True)
if side == 'right' or side == 'both':
  pi.setINDI('ao_indi_dx_ice.resume.arg', '1', wait=True)
