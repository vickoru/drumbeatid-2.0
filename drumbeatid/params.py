##
import os
from pathlib import Path

## CONSTANTS ##
FEATURE_LIST = ['spectrogram', 'mfccs', 'chroma', 'melspec']
# Alternative that does not resolve symlinks.
# ROOT_PATH = Path(__file__).absolute().parent
ROOT_PATH = Path(__file__).resolve().parent
PATH_DATA = ROOT_PATH.parent / 'data'
PATH_RAW_DATA = PATH_DATA / 'raw' / 'groove_test' ## TESTING
MODELS_PATH = ROOT_PATH / 'models'
IMAGES_PATH = ROOT_PATH / 'gui'

## VARIABLES ##
SAMPLE_INTERVAL = int(os.environ.get('SAMPLE_INTERVAL')) # Interval of the sample in seconds
SAMPLES_FOLDER_PATH = PATH_DATA.joinpath('processed',
                                        f'samples_{SAMPLE_INTERVAL}s')
MODEL_MODE = os.environ.get('MODEL_MODE')
print(SAMPLES_FOLDER_PATH)

## TESTS ##
AUDIO_TEST = os.environ.get('AUDIO_TEST')
AUDIO_TEST_FILEPATH = ROOT_PATH.parent / 'audio_samples' / AUDIO_TEST
