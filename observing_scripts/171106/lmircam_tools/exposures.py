from lmircam_tools import *

def get_lmircam_frames(dit, coadds, nseqs, 
                       inner_loop_max=10, 
                       save_data=True):
    dit = dit
    coadds = int(coadds)
    nseqs = int(nseqs)
    inner_loop_max = int(inner_loop_max)
    N_outer_loops = nseqs / inner_loop_max
    remainder = nseqs % inner_loop_max
    lbtintparams = (dit, coadds, inner_loop_max)

    pi.setINDI("LMIRCAM.Command.text", "0 contacq")
    if save_data:
        pi.setINDI("LMIRCAM.Command.text", "1 savedata")
    else:
        pi.setINDI("LMIRCAM.Command.text", "0 savedata")
    pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % lbtintparams, wait=True)

    for ii in xrange(N_outer_loops):
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*inner_loop_max),wait=True)
    if remainder > 0:
        pi.setINDI("LMIRCAM.Command.text", "%f %i %i lbtintpar" % (dit, coadds, remainder), wait=True)
        pi.setINDI("LMIRCAM.Command.text","go",timeout=(8*dit*coadds*nseqs),wait=True) 


