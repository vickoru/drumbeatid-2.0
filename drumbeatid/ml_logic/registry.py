from tensorflow.keras import models
import os

from drumbeatid.params import *

def load_model(model_mode=MODEL_MODE):
    '''
    Model modes:
    'basic'
    'reducedgenre'
    '''
    model_mode_path = os.path.join(MODELS_PATH, MODEL_MODE)
    # print(model_mode_path)
    model = models.load_model(model_mode_path)

    return model


def load_model_legacy(model_mode='reducedgenre'):
    '''
    Model modes:
    'basic'
    'reducedgenre'
    '''
    nm_model = f'model_{model_mode}'
    root_path = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(root_path, 'models', nm_model)
    print(model_path)
    model = models.load_model(model_path)

    return model
