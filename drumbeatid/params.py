##
import os

## VARIABLES ##

MODEL_MODE = os.environ.get('MODEL_MODE')

## CONSTANTS ##

FEATURE_LIST = ['spectrogram', 'mfccs', 'chroma', 'melspec']

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
print(ROOT_PATH)
MODELS_PATH = os.path.join(ROOT_PATH, 'models')
print(MODELS_PATH)
AUDIO_TEST = os.environ.get('AUDIO_TEST')
AUDIO_TEST_FILEPATH = os.path.join(
    ROOT_PATH, '..', 'audio_samples', AUDIO_TEST)
IMAGES_PATH = os.path.join(ROOT_PATH, 'gui')

# MODEL_MODE_PATH = os.path.join(MODELS_PATH, MODEL_MODE)
