import librosa


def padding(feat_matrix, size, axis):
    '''
    Function to pad and center a coefficients matrix of a sound feature using
    librosa functionalities
    '''

    padded = librosa.util.pad_center(feat_matrix, size=size, axis=axis)

    return padded
