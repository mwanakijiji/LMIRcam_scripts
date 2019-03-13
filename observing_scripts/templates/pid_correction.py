import pyfits

for framenum in range(7146,7165):

    print(framenum)
    file_name = 'lm_190224_'+str("{0:0>6d}".format(framenum))+'.fits'

    sciImg, header = pyfits.getdata(file_name,0,header=True)
    header["PID"] = 69

    hdu = pyfits.PrimaryHDU(sciImg, header=header)
    hdul = pyfits.HDUList([hdu])
    hdul.writeto(file_name, clobber=True)
    print('Saved ' + file_name)
