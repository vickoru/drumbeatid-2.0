from drumbeatid.ml_logic.preprocessor import preprocess
from drumbeatid.ml_logic.registry import load_model
from drumbeatid.utils.predictor import predict_genres
from drumbeatid.params import *

def main(audiofile):
    '''
    Main function to load the wav  file, load the model,
    preprocess the audio file and predict the genre
    '''

    X1, X2 = preprocess(audiofile=audiofile)

    model = load_model(model_mode=MODEL_MODE)

    y_pred = model.predict([X1, X2])
    # pred = np.argmax(y_pred)

    prediction = predict_genres(y_pred[0])

    if len(prediction) > 1:
        message = f'\nNot so sure about the style of your drumbeat 🤖\n It could be {", ".join(prediction[:-1]).capitalize()} or {prediction[-1].capitalize()}'
        return message

    message = f"The style of your drumbeat is:\
        {prediction[0].capitalize()}"

    return message

if __name__ == '__main__':
    print(main(AUDIO_TEST_FILEPATH))
