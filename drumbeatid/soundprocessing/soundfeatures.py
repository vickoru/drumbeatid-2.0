import numpy as np
import librosa
import os


class Audio:
    '''
    Librosa features coded in a class
    '''
    def __init__(self, audiofile, sr:int=22050, duration:int=6) -> np.array:
        '''
        Initialize class by getting the he waveforms and the sampling rate
        from librosa
        Default duration of the sample is 6 seconds, with a sampling rate of
        22050 samples per secong, default in librosa.
        '''
        max_length = duration * sr
        waveform_, samplingrate_ = librosa.load(
            audiofile, sr=sr, duration=duration)

        self.samplingrate = samplingrate_
        self.maxlength = max_length
        self.__file__ = audiofile
        self.__padded__ = False

        if waveform_.shape[0] < max_length:
            waveform_ = librosa.util.pad_center(
                waveform_, size=max_length, axis=0)
            self.__padded__ = True

        self.waveform = waveform_


    def calculate_spectrogramstft(self, nfft=2048, hoplength=512):
        '''
        ===  1 Spectrogram  ===
        requires 1-dimensional array x(timeseries), sampling rate sr
        returns spectrogram, a matplotlib.colormesh object

        '''
        #performing short time- Fourier analysis
        X = librosa.stft(self.waveform, n_fft=nfft, hop_length=hoplength)

        #amplitudes of given frequency at given time -> spectrogram
        self.Xdb = librosa.amplitude_to_db(abs(X))

        return self.Xdb


    def calculate_mfccs(self, number_coeffs=128):
        '''
        Calculate Mel frequency cepstral coefficients.
        Input:
        waveform: array representing the waveform originating from audio file
        samplingrate: sampling rate from audio
        number_coeffs: total number of coefficients to calculate, default is 20
        Output: array of mfccs
        '''
        self.mfccs = librosa.feature.mfcc(y=self.waveform, sr=self.samplingrate,
                                 n_mfcc=number_coeffs)

        return self.mfccs


    def calculate_chroma(self, nfft=2048, hoplength=512):
        '''
        Chroma Feature calculation with a hop length of 512 as default

        '''
        self.chromafeat = librosa.feature.chroma_stft(
            y=self.waveform, sr=self.samplingrate,
            n_fft=nfft, hop_length=hoplength)

        return self.chromafeat


    def calculate_melspec(self, nfft=2048, hoplength=512):
        '''
        Compute a mel-scaled spectrogram
        '''
        melspec = librosa.feature.melspectrogram(
            y=self.waveform, sr=self.samplingrate,
            n_fft=nfft, hop_length=hoplength)

        self.melspec_dB = librosa.power_to_db(melspec)

        return self.melspec_dB

    def get_all_features(self, padding=True):
        '''
        Calculate all features with the default settings, resulting in a
        dictionary containing the next key, value pairs
        'spectrogram': self.Xdb
        'mfccs': self.mfccs
        'chroma': self.chromafeat
        'melspec': self.melspec_db
        '''
        self.features = {
            'spectrogram': self.calculate_spectrogramstft(),
            'mfccs': self.calculate_mfccs(),
            'chroma': self.calculate_chroma(),
            'melspec': self.calculate_melspec()
            }

        if padding == True:
            self.features['chroma'] = librosa.util.pad_center(
                    self.features['chroma'],
                    size=self.features['mfccs'].shape[0], axis=0
                        )

        return self
