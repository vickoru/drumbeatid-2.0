from email import contentmanager
import re
from fastapi import FastAPI, UploadFile, File
from starlette.responses import Response
# from librosa import load
# from librosa.util import valid_audio
# import librosa
import numpy as np
import io
import sys
import os

# loc = os.getcwd()
# path2 = os.path.join(loc, '..', '..')
# sys.path.append(path2)
# print(os.getcwd())

from drumbeatid.ml_logic.registry import load_model
from drumbeatid.ml_logic.preprocessor import process, process_audiofile
from drumbeatid.ml_logic.dictionary import predict_genres


#from main_functions import bla bla bl
# from working_functions import reading_audiofile, spectogram,
#                           get_add_features, add_features_as_array_for_CNN

app = FastAPI()

app.state.model = load_model(model_mode='reducedgenre')


@app.get("/")
def index():
    return {"status": "ok"}

@app.post('/upload_wav')
async def receive_wav(wav: bytes=File(...)):
    ### Receiving the wav file

    dict_genres = {10: 'Rock'}

    x, sr = process_audiofile(io.BytesIO(wav))

    X1, X2 = process(x, sr)
    print(X1.shape, X2.shape)

    y_pred = app.state.model.predict([X1, X2])
    print(y_pred)
    # pred = np.argmax(y_pred)
    # print(pred)
    prediction = predict_genres(y_pred[0])
    print(prediction)

    return {'genre': prediction}


    # check_audio = valid_audio(x)

    # resp = Response(content=str(check_audio))

    # if check_audio == True:
    #     return x, sr
    # else:
    #     return print('Not possible')

    # preprocess x -> spectogram
    # spectogram = spectogram(x, sr)

    # preprocess x -> add features
    # mfcc, specbandwith, spectralcentroid, chroma, zerocrossrate, spectralroff = get_add_features(x,sr)
    # ### !!!! normalize those features ? Yes think so ! How? ===
    # feat_array = np.concatenate(mfcc, specbandwith, spectralcentroid, chroma,
    #                             zerocrossrate, spectralroff)


    # send preprocessed data to prediction
    # predict_cnn = model_cnn.predict(spectogram)
    # predict_ml = model_ml.predict(feat_array)

    # return prediction
    # return Response(class_cnn=predict_cnn, class_ml=predict_ml)

    # return x, sr

# @app.get("/predict")
# def predict(waveform=np.array([0]), samplingrate=0):      # 1
#     """
#     we use type hinting to indicate the data types expected
#     for the parameters of the function
#     FastAPI uses this information in order to hand errors
#     to the developpers providing incompatible parameters
#     FastAPI also provides variables of the expected data type to use
#     without type hinting we need to manually convert
#     the parameters of the functions which are all received as strings
#     """

#     # X_pred = pd.DataFrame(dict(
#     #     key=[pd.to_datetime(pickup_datetime)],  # useless but the pipeline requires it
#     #     pickup_datetime=[pd.to_datetime(pickup_datetime)],
#     #     pickup_longitude=[float(pickup_longitude)],
#     #     pickup_latitude=[float(pickup_latitude)],
#     #     dropoff_longitude=[float(dropoff_longitude)],
#     #     dropoff_latitude=[float(dropoff_latitude)],
#     #     passenger_count=[int(passenger_count)]))

#     # model = load_model()

#     # X_processed = preprocess_features(X_pred)

#     waveform, samplingrate = receive_wav()

#     y_pred = app.state.model.predict(waveform, samplingrate)

#     return {'genre': str(y_pred)}
