import numpy as np
import pickle
from sklearn.base import TransformerMixin, BaseEstimator


class CustomMinMaxScaler(TransformerMixin, BaseEstimator):
    '''
    Custom MinMax scaler class for spectrograms, based on the training data used.
    Min and max values are hard encoded.

    feature: required for initialization. It is a string that refers to the
    feature to be scaled
    'spectrogram': Fourier transform of the soundwave
    'mfccs': Mel frequency cepstral coefficients
    'chroma': Chroma features
    'melspect': Mel-scale spectrogram

    .fit() method only returns the hard encoded  Input: Matrix of values
    of a spectrogram

    .transform transforms the given matrix according to the hard-encoded values

    Input: Array of coefficients for a spectrogram
    Output: Scaled array according to the hard-encoded values
    '''

    def __init__(self, feature):
        self.feature = feature


    def fit(self):
        '''
        Unlike a regular .fit method, this method returns a dictionary of
        hard-encoded values for each spectrogram according to the trained model
        '''
        try:
            with open('scale_dict.pickle', 'rb') as f:
                scaler_dict = pickle.load(f)
        except:
            scaler_dict = {
                'spectrogram': (-83.33994, 47.971237),
                'mfccs': (-1078.5714, 153.1723),
                'melspec': (-95.333145, 34.96595),
                'chroma': (0.0, 1.0)
                }
        self.scaling_coeff = scaler_dict[self.feature]
        return self


    def transform(self, X):

        max_ = self.scaling_coeff[1]
        min_ = self.scaling_coeff[0]
        norm = np.array((X - min_)/(max_ - min_))

        return norm
