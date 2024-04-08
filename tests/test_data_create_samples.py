import pandas as pd
import unittest

from drumbeatid.data.sample_processing import create_samples_folder, create_samples_from_segment
from drumbeatid.data.main_data import create_audio_samples_from_df
from drumbeatid.params import *


class TestCreateAudioSamples(unittest.TestCase):
    def test_create_samples_previous_false(self):
        audio_df = pd.read_csv(PATH_RAW_DATA / 'info_audiosamples.csv')
        create_audio_samples_from_df(audio_df=audio_df, remove_previous=False)
