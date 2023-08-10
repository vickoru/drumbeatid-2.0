##
import numpy as np
from drumbeatid.params import *


def predict_genres(probabilites, threshold=0.15,
                   model_mode=MODEL_MODE):
    '''
    Function to predict the drumming style given an array of
    probabilities.
    Output corresponds to drumming styles that are apart by threshold
    in terms of probability.
    '''

    max_ = np.round(np.max(probabilites), 3)
    difference = threshold
    indexes = []
    for idx, value in enumerate(probabilites):
        calcdif = max_ - np.round(value, 3)
        if calcdif <= difference:
            indexes.append(idx)

    prediction = []
    for idx in indexes:
        prediction.append(
            dictionary_genres(idx, model_mode)
            )

    return prediction

def dictionary_genres(idx, model_mode=MODEL_MODE):
    if model_mode == 'reducedgenre':
        dict_genres = {
            0: 'funk',
            1: 'hiphop',
            2: 'jazz',
            3: 'latin',
            4: 'rock',
            5:  'soul'
        }
    else:
        dict_genres = {0: 'afrobeat',
                    1: 'afrocuban',
                    2: 'blues',
                    3: 'country',
                    4: 'dance',
                    5: 'funk',
                    6: 'gospel',
                    7: 'hiphop',
                    8: 'jazz',
                    9: 'latin',
                    10: 'middleeastern',
                    11: 'neworleans',
                    12: 'pop',
                    13: 'punk',
                    14: 'reggae',
                    15: 'rock',
                    16: 'soul'}

    return dict_genres[idx]
