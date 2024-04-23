##
import os
from pathlib import Path

def define_env(gdrive='/content/drive'):
    '''
    Defining environment to execute.
    Valid options are 'local', 'colab', 'gcp'.
    The ROOT_PATH is defined according to the ENV.
    '''
    validenvs = ['local', 'colab', 'gcp']

    try:
        envmode = os.environ['ENV_MODE']

    except KeyError as error:
        print(error)
        print("Reverting to 'local' environment")
        envmode = 'local'

    finally:

        # if envmode not in validenvs:
        #     raise Exception(f'{envmode} is not a valid environment option')

        if envmode == 'local':
            data_path = ROOT_PATH.parent / 'data'

        elif envmode == 'colab':
            data_path =  Path(gdrive) / 'MyDrive' / 'drumbeatid' / 'data'

        else:
            raise Exception('No valid environment option '
                                    f'for "{envmode}" was found')

    return envmode, data_path


## CONSTANTS ##
FEATURE_LIST = ['spectrogram', 'mfccs', 'chroma', 'melspec']
# ROOT_PATH = Path(__file__).absolute().parent # Alternative that
# does not resolve symlinks.
ROOT_PATH = Path(__file__).resolve().parent
ENV_MODE, DATA_PATH  = define_env()
RAW_DATA_PATH = DATA_PATH / 'raw'
MODELS_PATH = ROOT_PATH / 'models'
IMAGES_PATH = ROOT_PATH / 'gui'


## VARIABLES ##
SAMPLE_INTERVAL = int(os.environ.get('SAMPLE_INTERVAL')) # Interval of the sample in seconds
SAMPLES_FOLDER_PATH = DATA_PATH.joinpath('processed',
                                        f'samples_{SAMPLE_INTERVAL}s')
MODEL_MODE = os.environ.get('MODEL_MODE')


## TESTS ##
AUDIO_TEST = os.environ.get('AUDIO_TEST')
AUDIO_TEST_FILEPATH = ROOT_PATH.parent / 'audio_samples' / AUDIO_TEST
