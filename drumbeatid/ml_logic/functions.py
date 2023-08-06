import numpy as np
import librosa
import os


def calculate_mfccs(waveform, samplingrate, number_coeffs=128):
    '''
    Caluculate Mel frequency cepstral coefficients.
    Input:
    waveform: array representing the waveform originating from audio file
    samplingrate: sampling rate from audio
    number_coeffs: total number of coefficients to calculate, default is 20
    Output: array of mfccs
    '''
    mfccs = librosa.feature.mfcc(y=waveform, sr=samplingrate,
                                 n_mfcc=number_coeffs)
    return mfccs


def calculate_specbandwidth(waveform, samplingrate, order_p=2):
    '''
    Calculates spectral bandwithd of oder p
    '''
    specbw = librosa.feature.spectral_bandwidth(y=waveform, sr=samplingrate,
                                                p=order_p)

    return specbw


def calculate_spectralcentroid(waveform, samplingrate, nfft=2048, hoplength=512):
    '''
    Calculate spectral centroid
    '''
    specent = librosa.feature.spectral_centroid(y=waveform,
                                                sr=samplingrate, n_fft=nfft,
                                                hop_length=hoplength)

    return specent


def calculate_chroma(waveform, samplingrate, nfft=2048, hoplength=512):
    '''
    Chroma Feature calculation with a hop length of 512 as default

    '''
    chromafeat = librosa.feature.chroma_stft(y=waveform, sr=samplingrate,
                                             n_fft=nfft,
                                             hop_length=hoplength)

    return chromafeat


def calculate_zerocrossrate(waveform, framelength=2048, hoplength=512):
    '''
    Caluculate Zero crossing rate.

    '''
    zerocr = librosa.feature.zero_crossing_rate(y=waveform, frame_length=framelength,
                                                hop_length=hoplength)

    return zerocr


def calculate_spectralroff(waveform, samplingrate, nfft=2048, hoplength=512):
    '''
    Calculate spectral roll off of the waveform
    '''
    specroff = librosa.feature.spectral_rolloff(y=waveform,
                                                sr=samplingrate, n_fft=nfft,
                                                hop_length=hoplength)

    return specroff

def read_audio(audiofile_path, samplingrate=22050, duration=None):
    '''
    Reading in audiofile, returns 1-dimensional array x, sampling rate sr
    '''

    x , sr = librosa.load(audiofile_path, sr=samplingrate, duration=duration)
    return x, sr


def calculate_spectogram(waveform, nfft=2048, hoplength=512):
    '''
    ===  1 Spectogram  ===
    requires 1-dimensional array x(timeseries), sampling rate sr
    returns spectogram, a matplotlib.colormesh object

    '''

    #performing short time- Fourier analysis
    X = librosa.stft(waveform, n_fft=nfft, hop_length=hoplength)

    #amplitudes of given frequency at given time -> spectrogram
    Xdb = librosa.amplitude_to_db(abs(X))

    #plt.figure(figsize=(6, 5), frameon=False)
    #librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz') # for demonstration purposes

#     spectogram = librosa.display.specshow(Xdb, sr=sr, x_axis=None, y_axis=None) # without axes

    return Xdb

def calculate_melspect(waveform, samplingrate, nfft=2048, hoplength=512):

    melspec = librosa.feature.melspectrogram(y=waveform, sr=samplingrate, n_fft=nfft, hop_length=hoplength)

    melspec_dB = librosa.power_to_db(melspec)

    return melspec_dB

def padding(feat_matrix, size, axis):

    padded = librosa.util.pad_center(feat_matrix, size=size, axis=axis)

    return padded


def padding_waveforms(waveforms, max_length=132300, axis=0):
    newwaveforms = np.zeros(waveforms.shape)
    for idx, values in enumerate(waveforms):
        if values.shape[0] < max_length:
            newwaveforms[idx] = librosa.util.pad_center(waveforms[idx], size=max_length, axis=axis)

    return np.array(newwaveforms)


# def minmaxscaling(matrix):
#     max_ = np.max(matrix)
#     min_ = np.min(matrix)
#     norm = np.array((matrix - min_)/(max_ - min_))

#     return norm

def minmaxscaling(matrix, var, mode):
    '''
    requires as input: matrix: a matrix with values of same variable)
                       var (as string) name of the variable in the matrix (e.g. spectralroff)
                       mode: "fit_transform" fits the min_max_scaler with the given values and stores
                                              the min and max into a dictionary (scaler_dict).
                                             Then transforms (normalizes) the given array

                             "transform" transforms the given matrix according to previously stored values

                output: transformed matrix
    '''

    if mode == "fit_transform":
        try:
            with open('scaler_dict.pickle', 'rb') as handle:
                scaler_dict = pickle.load(handle)
        except:
            scaler_dict = {
                'spectrogram': (47.971237, -83.33994),
                'mfccs': (153.1723, -1078.5714),
                'melspec': (34.96595, -95.333145),
                'chroma': (1.0, 0.0)
                }
        max_ = np.max(matrix)
        min_ = np.min(matrix)
        scaler_dict[(var + "max")] = max_
        scaler_dict[(var + "min")] = min_
        norm = np.array((matrix - min_)/(max_ - min_))

        with open('scaler_dict.pickle', 'wb') as shandle:
            pickle.dump(scaler_dict, shandle, protocol=pickle.HIGHEST_PROTOCOL)

        return norm

    if mode == "transform":
        scaler_dict = {
                'spectrogram': (47.971237, -83.33994),
                'mfccs': (153.1723, -1078.5714),
                'melspec': (34.96595, -95.333145),
                'chroma': (1.0, 0.0)
                }

        # with open('scaler_dict.pickle', 'rb') as handle:
        #     scaler_dict = pickle.load(handle)

        max_ = scaler_dict[var][0]
        min_ = scaler_dict[var][1]
        norm = np.array((matrix - min_)/(max_ - min_))

        return norm


def processing_drummers(dataframe):
    df_drummers = dataframe.drop(columns=['drummer', 'id', 'session', 'split', 'midi_filename'])
    df_drummers = df_drummers.dropna()
    df_drummers = df_drummers[df_drummers['beat_type'] == 'beat']
    df_drummers['style_new'] = df_drummers['style'].apply(lambda x: x.split('/')[0])
    df_drummers['style'] = df_drummers['style_new']

    return df_drummers.drop(columns='style_new')


def process_audiofiles(loc, drummers_df, samplingrate=22050, duration=6):

    waveforms_ = drummers_df['audio_filename'].apply(
        lambda x: librosa.load(os.path.join(loc, x), sr=samplingrate, duration=duration)).values
    genres = drummers_df['style'].values

    waveforms = []
    sr = []
    for values in waveforms_:
        waveforms.append(values[0])
        sr.append(values[1])

    waveforms_padded = padding_waveforms(waveforms, max_length=132300, axis=0)

    return waveforms_padded, np.array(sr), genres


def spectogram_mfccs(waveform, sr):
    mfccs = []
    for idx in range(waveform.shape[0]):
        mfccs.append(calculate_mfccs(waveform[idx], sr[idx], number_coeffs=128)) # mfccs

    return np.array(mfccs)


def spectogram_chroma(waveform, sr):
    chroma = []
    for idx in range(waveform.shape[0]):
        chroma.append(calculate_chroma(waveform[idx], samplingrate=sr[idx]))

    return np.array(chroma)


def spectogram_stft(waveform):
    spectogram_feat = []
    for idx in range(waveform.shape[0]):
        spectogram_feat.append(calculate_spectogram(waveform[idx]))

    return np.array(spectogram_feat)


def spectogram_mel(waveform, sr):
    melspect = []
    for idx in range(waveform.shape[0]):
        melspect.append(calculate_melspect(waveform[idx], samplingrate=sr[idx]))

    return np.array(melspect)
