from importlib.util import spec_from_file_location
from inspect import stack
import wave


import numpy as np
import librosa

from drumbeatid.ml_logic.functions import spectogram_mfccs, spectogram_stft, spectogram_mel
from drumbeatid.ml_logic.functions import spectogram_chroma, padding, minmaxscaling, padding_waveforms

def process_audiofile(audiofile):

    waveform, samplingrate = librosa.load(audiofile, duration=6)

    return waveform, samplingrate


def process(waveform, samplingrate, max_length=132300):

    if waveform.shape[0] < max_length:
        waveform = librosa.util.pad_center(waveform, size=max_length, axis=0)

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
