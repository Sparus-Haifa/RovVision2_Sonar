from scipy.signal import argrelextrema
import numpy as np

def rope_detect(prev_col,extrema,start_row,nrows,im):
    imt=im[start_row:start_row+nrows,:].sum(axis=0).flatten().astype(float)
    #plt.plot(np.convolve(im1,np.concatenate((np.ones(8),-np.ones(8)))))
    #conv_val=10
    #im2=np.convolve(im1,np.ones(conv_val),'valid')
    yy=np.fft.fft(imt)
    clear_freqs=5
    yy[clear_freqs:-clear_freqs]=0
    im2r=np.fft.ifft(yy)
    
    maxima=argrelextrema(im2r, np.greater)[0]
    minima=argrelextrema(im2r, np.less)[0]
    if extrema is None:
        totest=np.concatenate((maxima,minima))
    elif extrema == 'max':
        totest=maxima
    else:
        totest=minima
    if len(totest)==0:
        return None
    new_col=totest[np.argmin(np.abs(totest-prev_col))]
    res='min'
    if new_col in maxima:
        res='max'
    return res,new_col