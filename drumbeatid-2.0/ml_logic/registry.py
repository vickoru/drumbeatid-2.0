from tensorflow.keras import Model, models
import os


def load_model(model_mode='reducedgenre'):
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
