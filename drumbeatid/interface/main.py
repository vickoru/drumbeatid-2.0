
import pandas as pd

from colorama import Fore, Style

from drumbeatid.data.sample_processing import create_audio_samples_from_df
from drumbeatid.ml_logic.preprocessor import preprocess
from drumbeatid.utils.predictor import predict_genres
from drumbeatid.params import *


def create_samples(remove_previous=False):
    """
    The function `create_samples` reads audio information from a CSV file, creates
    audio samples, and saves the info of the generated samples to a new CSV file.

    :param remove_previous: The `remove_previous` parameter in the `create_samples`
    function is a boolean parameter that specifies whether to remove any previously
    created samples before creating new ones. If `remove_previous` is set to `True`,
    any existing samples will be deleted before creating new ones.
    defaults to False (optional)

    :return: None
    """
    audio_df = pd.read_csv(RAW_DATA_PATH / '..' / 'info_test.csv')
    samples_df = create_audio_samples_from_df(
        audio_df=audio_df, remove_previous=remove_previous)
    df_csv_path = SAMPLES_FOLDER_PATH.parent / (SAMPLES_FOLDER_PATH.stem + '.csv')
    samples_df.to_csv(df_csv_path, index=False)

    return None


def predict(audiofile):
    '''
    Main function to load the wav  file, load the model,
    preprocess the audio file and predict the genre
    '''

    from drumbeatid.ml_logic.registry import load_model

    X1, X2 = preprocess(audiofile=audiofile)

    model = load_model(model_mode=MODEL_MODE)

    y_pred = model.predict([X1, X2])
    # pred = np.argmax(y_pred)

    prediction = predict_genres(y_pred[0])

    if len(prediction) > 1:
        message = (f'\nNot so sure about the style of your drumbeat 🤖\n'
                   'It could be {", ".join(prediction[:-1]).capitalize()} '
                   'or {prediction[-1].capitalize()}')
        return message

    message = f"The style of your drumbeat is:\
        {prediction[0].capitalize()}"

    return message


if __name__ == '__main__':
    # print(predict(AUDIO_TEST_FILEPATH))
    create_samples(remove_previous=True)
