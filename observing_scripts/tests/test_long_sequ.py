from pyindi import *
pi = PyINDI(verbose=False)

dit = 0.0
coadds = 1 # this should probably be 1
nseqs = 100
use_bg = 1

for ii in range(0, 50):
  print(ii)
  pi.setINDI("LMIRCAM.acquire.int_time=%f;num_coadds=%i;num_seqs=%i;enable_bg=%i;is_bg=0;is_cont=0"%(dit, coadds, nseqs, use_bg), timeout = 3.0 * dit * nseqs)
