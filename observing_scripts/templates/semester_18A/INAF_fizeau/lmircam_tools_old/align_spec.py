import pyfits
import numpy as np
from lmircam_tools import pi
from lmircam_tools.exposures import get_lmircam_frames
from datetime import datetime
from time import sleep
import glob

def align_spec(nod_pos):
  
  if nod_pos == 'LEFT':
    channel_left = 641
    channel_right = 767
  if nod_pos == 'RIGHT':
    channel_left = 769
    channel_right = 895
  
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=specoverlap;Comment=type of data obtained in fizeau mode.')
  
  xoff = 0.75             
  date = str(datetime.utcnow().year)[2:] + str(datetime.utcnow().month).zfill(2) + str(datetime.utcnow().day).zfill(2)
  
  pi.setINDI('Acromag.FPC.Tip=0;Tilt=' + str(-xoff) + ';Piston=0;Mode=1')
  
  filelist = glob.glob('/mnt/iscsi/lmircam/L0/'+date+'/lm_*.fits')
  if len(filelist) == 0: file_number = 0
  else: file_number = int(np.sort(filelist)[-1][-11:-5])
  
  get_lmircam_frames(0.0, 1, 1, inner_loop_max = 10)
  file_number = file_number + 1
  sleep(0.005)
  frame = pyfits.open('/mnt/iscsi/lmircam/L0/'+date+'/lm_' + date + '_' + str(file_number).zfill(6) + '.fits')['Primary'].data.astype(np.float)
  
  cut = np.median(frame, axis=0)[channel_left:channel_right]
  cut = (cut - np.median(cut[np.where(cut<np.median(cut)+3.0*np.std(cut))]))**2.0
  x = np.arange(channel_left, channel_right).astype(np.float)
  
  pos0 = np.sum(cut[0:40] * x[0:40]) / np.sum(cut[0:40])
  pos1 = np.sum(cut[43:83] * x[43:83]) / np.sum(cut[43:83])
  
  pi.setINDI('Acromag.FPC.Tip=0;Tilt=' + str(2.0 * xoff) + ';Piston=0;Mode=1')
  
  get_lmircam_frames(0.0, 1, 1, inner_loop_max = 10)
  file_number = file_number + 1
  sleep(0.005)
  frame = pyfits.open('/mnt/iscsi/lmircam/L0/'+date+'/lm_' + date + '_' + str(file_number).zfill(6) + '.fits')['Primary'].data.astype(np.float)
  
  cut = np.median(frame, axis=0)[channel_left:channel_right]
  cut = (cut - np.median(cut[np.where(cut<np.median(cut)+3.0*np.std(cut))]))**2.0
  x = np.arange(channel_left, channel_right).astype(np.float)
  
  pos2 = np.sum(cut[86:126] * x[86:126]) / np.sum(cut[86:126])
  
  xoff_overlap = 2.0 * xoff / (pos2 - pos0) * (pos1 - pos2)
  
  pi.setINDI('Acromag.FPC.Tip=0;Tilt=' + str(xoff_overlap) + ';Piston=0;Mode=1')
  
  pi.setINDI('LMIRCAM.EditFITS.Keyword=dataflag;Value=N/A;Comment=type of data obtained in fizeau mode.')
  
  pi.setINDI("LMIRCAM.Command.text", "0 savedata")
  pi.setINDI("LMIRCAM.Command.text", "1 contacq")
