import numpy as np

def predict(waveform, samplingrate):

    if waveform.shape[0] > 1:
        return 'Rock'
    else:
        return 'Not known'
