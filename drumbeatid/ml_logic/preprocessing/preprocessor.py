from importlib.util import spec_from_file_location
from inspect import stack

import numpy as np
import librosa

from drumbeatid.soundprocessing.soundfeatures import Audio
from drumbeatid.utils.utilities import padding

def preprocess(audiofile, samplingrate=22050, duration=6):
    '''
    Preprocessing function to prepare spectrograms as input for the model
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



    waveforms = np.array([waveform])
    sr = np.array([samplingrate])

    mfccs = spectogram_mfccs(waveforms, sr)
    spectrogram_feat = spectogram_stft(waveforms)
    melspect = spectogram_mel(waveforms, sr)
    chroma = spectogram_chroma(waveforms, sr)

    chroma_padded = padding(chroma, size=mfccs.shape[1], axis=1)

    spectogram_feat_norm = minmaxscaling(
        spectrogram_feat, var='spectrogram', mode='transform' )
    mfccs_norm = minmaxscaling(mfccs, var='mfccs', mode='transform')
    melspect_norm = minmaxscaling(melspect, var='melspec', mode='transform')
    chroma_padded_norm = minmaxscaling(chroma_padded, var='chroma', mode='transform')

    # spectogram_feat_norm = minmaxscaling(spectrogram_feat)
    # mfccs_norm = minmaxscaling(mfccs)
    # melspect_norm = minmaxscaling(melspect)
    # chroma_padded_norm = minmaxscaling(chroma_padded)

    stacked = librosa.util.stack([mfccs_norm, melspect_norm,
                                  chroma_padded_norm], axis=3)
    spectogram_feat_norm = np.expand_dims(spectogram_feat_norm, axis=-1)

    return spectogram_feat_norm, stacked

# path = '/Users/HZB/code/vickoru/drumbeatid/raw_data/groove/drummer1/session1/204_rock-halftime_140_fill_4-4.wav'

# y, sr = librosa.load(path, duration=6)

# X1, X2 = process(y, sr)
# print(X1.shape)
# print(X2.shape)
