##
import os

## VARIABLES ##

MODEL_MODE = os.environ.get('MODEL_MODE')

## CONSTANTS ##

FEATURE_LIST = ['spectrogram', 'mfccs', 'chroma', 'melspec']


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
MODELS_PATH = os.path.join(ROOT_PATH, 'models')

MODEL_MODE_PATH = os.path.join(MODELS_PATH, MODEL_MODE)
print(MODEL_MODE_PATH)
