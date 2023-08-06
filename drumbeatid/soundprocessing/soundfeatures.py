import numpy as np
import librosa
import os

from drumbeatid.ml_logic.preprocessor import Audio

class Audio:
    '''
    Librosa features coded in a class
    '''
    def __init__(self, audiofile, duration=6):
        ## Get the waveforms and the sampling rate from class Audio
        self.waveform, self.samplingrate = librosa.load(
            audiofile, duration=duration)

    def calculate_mfccs(self, number_coeffs=128):
        '''
        Caluculate Mel frequency cepstral coefficients.
        Input:
        waveform: array representing the waveform originating from audio file
        samplingrate: sampling rate from audio
        number_coeffs: total number of coefficients to calculate, default is 20
        Output: array of mfccs
        '''
        self.mfccs = librosa.feature.mfcc(y=self.waveform, sr=self.samplingrate,
                                 n_mfcc=number_coeffs)


    def calculate_spectrogram(self, nfft=2048, hoplength=512):
        '''
        ===  1 Spectogram  ===
        requires 1-dimensional array x(timeseries), sampling rate sr
        returns spectogram, a matplotlib.colormesh object

        '''
        #performing short time- Fourier analysis
        X = librosa.stft(self.waveform, n_fft=nfft, hop_length=hoplength)

        #amplitudes of given frequency at given time -> spectrogram
        self.Xdb = librosa.amplitude_to_db(abs(X))

        return self.Xdb
