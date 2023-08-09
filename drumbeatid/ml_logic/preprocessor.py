from importlib.util import spec_from_file_location
from inspect import stack

import numpy as np
import librosa

from drumbeatid.params import *
from drumbeatid.soundprocessing.soundfeatures import Audio
from drumbeatid.utils.minmaxscaler import CustomMinMaxScaler


def preprocess(audiofile, samplingrate=22050, duration=6):
    '''
    Preprocessing function to prepare spectrograms as input for the model.

    Input:
        audiofile: audiofile in format .wav is only implemented for the moment
        samplingrate: samples per second to load the file using librosa
        duration: maximum duration in seconds to take from the audiofile,
                    default set to 6 seconds
    '''

    audio = Audio(audiofile=audiofile,  sr=samplingrate, duration=duration)
    audio.get_all_features()

    waveform = audio.waveform
    sr_ = audio.samplingrate

    audio.get_all_features()

    spectrogram_list = FEATURE_LIST
    dict_spectrogram = {}

    for feature_ in spectrogram_list:
        scaler_ = CustomMinMaxScaler(feature=feature_)
        scaler_.fit()
        dict_spectrogram[feature_] = scaler_.transform(audio.features[feature_])

    feat_stacked = librosa.util.stack([
        dict_spectrogram['mfccs'],
        dict_spectrogram['melspec'],
        dict_spectrogram['chroma']
        ], axis=2)

    feat_spec = np.expand_dims(dict_spectrogram['spectrogram'], axis=-1)

    return feat_spec, feat_stacked
