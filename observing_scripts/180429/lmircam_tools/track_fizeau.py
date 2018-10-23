from lmircam_tools import *
import pyfits
import numpy as np
from lmircam_tools import pi
from datetime import datetime
from time import sleep
import glob
import os.path

gain = 1.0
conv_mic_enc = 50.0

def track_spectral_fringes(nod_pos, band):
  if band == 'lband':
    lspec = 300     # length of the usable spectrum in pix
    lam_lo = 2.9    # lower end of usable spectrum in micron
    lam_hi = 4.0    # upper end of usable spectrum in micron
  if band == 'mband':
    lspec = 150     # length of the usable spectrum in pix
    lam_lo = 4.5    # lower end of usable spectrum in micron
    lam_hi = 5.0    # upper end of usable spectrum in micron
  lastframe = 'none'
  
  date = str(datetime.utcnow().year)[2:] + str(datetime.utcnow().month).zfill(2) + str(datetime.utcnow().day).zfill(2)
  
  filelist = glob.glob('/mnt/iscsi/lmircam/L0/'+date+'/lm_*.fits')
  if len(filelist) == 0: file_number = 0
  else: file_number = int(np.sort(filelist)[-1][-11:-5])
  
  while True:
    file_number = file_number + 1
    tstart = datetime.now()
    if nod_pos == 'LEFT':
      channel_left = 641
      channel_right = 766
    if nod_pos == 'RIGHT':
      channel_left = 769
      channel_right = 894
    
    while True:
      if not os.path.isfile('/mnt/iscsi/lmircam/L0/'+date+'/lm_' + date + '_' + str(file_number).zfill(6) + '.fits')
        print 'Sleeping 10ms'
        sleep(0.01)
        continue
    while True:
      if os.path.isfile('/mnt/iscsi/lmircam/L0/'+date+'/lm_' + date + '_' + str(file_number+1).zfill(6) + '.fits')
          file_number = file_number + 1
      else:
        break
    
    sleep(0.005)
    frame = pyfits.open('/mnt/iscsi/lmircam/L0/'+date+'/lm_' + date + '_' + str(file_number).zfill(6) + '.fits')['Primary'].data.astype(np.float)
    frame = frame[:, channel_left:channel_right)
    
    amp = np.abs(np.fft.fftshift(np.fft.fft2(frame)))[:, 62:]
    amp = amp - np.median(amp[50:, 2:])
    
    amp_mask = amp * 0.0
    amp_mask[np.where(amp > 5.0 * np.std(amp[0:50, 14:54]))] = amp[np.where(amp > 5.0 * np.std(amp[0:50, 14:54]))]
    
    ypix = np.arange(130, 171)
    xpix = np.arange(20, 37)
    
    angles = [] # tangens of angle of fringes from vertical
    for x in xpix:
      ypos = np.sum(amp_mask[130:171, x] * ypix) / np.sum(column) - 150.0
      angles.append(ypos/np.float(x))
    
    tan_alpha = np.median(np.array(angles))
    print np.arctan(tan_alpha)
    tend = datetime.now()
    print tend-tstart
    
    path = np.float(lspec) * tan_alpha / (lam_lo / 14.4 * 18.75) * lam_lo * lam_hi / (lam_hi - lam_lo) * gain
    if path >= 0: path = '>' + str(path * conv_mic_enc)
    elif path < 0: path = '<' + str(path * conv_mic_enc)
    else:
      print 'WARNING: Invalid path not sent to SPC.'
      continue
    
    ?pi.setINDI('Ubcs.SPC_Trans.command' + str(path) + ';Mode=1')
