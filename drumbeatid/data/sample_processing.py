import numpy as np
import pandas as pd

from pathlib import Path
import shutil

from pydub import AudioSegment

from colorama import Fore, Style
from tqdm import tqdm

from drumbeatid.params import *

class SamplesProcessing():
    '''
    '''
    def __init__(self, audio_raw_df:pd.DataFrame, filename:str=None) -> None:
        '''
        :param
        :param filename: csv filename with columns 'style', 'audio_filename'. (Optional)

        :return audio_raw_df: pandas dataframe with columns 'style', 'audio_filename'
        and 'duration'

        '''
        if filename:
            filename = Path(filename)
            filename_path = RAW_DATA_PATH / 'raw' / filename
            self.__audio_raw_file__ = filename_path
            self.audio_raw_df = pd.read_csv(filename_path)
        else:
            self.audio_raw_df = audio_raw_df

        self.styles = list(audio_raw_df['style'].unique())



    def create_samples_folder(styles:list, remove_previous:bool=False,
                        gdrive='/content/drive') -> str:
        """
        The function `create_samples_folder` creates a folder structure for generating
        audio samples based on specified styles, with an option to remove previous
        samples if needed.

        :param styles: The `styles` parameter in the `create_samples_folder` function is
        a list that contains the different styles for which you want to create sample
        folders. Each element in the list represents a specific style for which a folder
        will be created within the main samples folder.
        :type styles: list

        :param remove_previous: The `remove_previous` parameter in the
        `create_samples_folder` function is a boolean flag that determines whether to
        remove the previous samples folder before creating a new one. If set to `True`,
        the function will check if the samples folder exists and remove it before
        creating a new folder structure for the samples, defaults to False.
        :type remove_previous: bool (optional)

        :param gdrive: The `gdrive` parameter in the `create_samples_folder` function is
        a default parameter that specifies the Google Drive path where the samples
        folder will be created. By default, it is set to `'/content/drive'`. This
        parameter allows you to specify a different Google Drive path if needed.
        defaults to /content/drive (optional)

        :return: The function `create_samples_folder` is returning `None`.
        """

        if remove_previous:
            if not SAMPLES_FOLDER_PATH.exists():

                raise FileNotFoundError(f'The folder {SAMPLES_FOLDER_PATH} does '
                                'not exist, so there is nothing to remove. '
                                'Please verify that you want to remove a previous '
                                'folder of samples.')

            shutil.rmtree(SAMPLES_FOLDER_PATH)

            print(Fore.GREEN + Style.BRIGHT + '\nOverwriting...\n' + Style.RESET_ALL)


        try:
            SAMPLES_FOLDER_PATH.mkdir(parents=True)

            try:
                for style in styles:
                    style_folder = SAMPLES_FOLDER_PATH.joinpath(style)
                    style_folder.mkdir()

            except FileExistsError as error:
                print(error)
                print(f'The folder for the style {style} already exists. '
                    'Please verify that the sample duration you have chosen has '
                    'not already been processed.')
                raise

        except FileExistsError as error:
            print(error)
            print('The folder already exists. Please verify '
                'that the sample duration you have chosen has not already '
                'been processed.')
            raise
    #         return f'The folder already exists. Please verify that the sample duration you have chosen has not already been processed.'

        else:
            print(f'\n{Fore.BLUE + Style.BRIGHT }The folder for the samples '
                f'has been successfully created!{Style.RESET_ALL}\n')

        return


    def create_samples_from_segment(drum_entry:pd.Series,
                                SAMPLE_INTERVAL:int=SAMPLE_INTERVAL) -> pd.DataFrame:
        """
        The function `create_samples_from_segment` generates samples from a given audio
        segment and returns a DataFrame with information about each generated sample.

        :param drum_entry: The `drum_entry` parameter is a pandas Series containing
        information about a specific drum entry. Each entry must include 'style' and
        'audio_filename' as columns. This function takes this drum entry
        information and creates samples from the corresponding audio file based on the
        specified `SAMPLE_INTERVAL`.
        :type drum_entry: pd.Series

        :param SAMPLE_INTERVAL: The `SAMPLE_INTERVAL` parameter represents the interval
        at which you want to sample the audio segment. It is specified in milliseconds.
        This parameter determines the size of each sample that will be extracted from
        the audio segment. It is defined as environment variable.
        :type SAMPLE_INTERVAL: int

        :return: The function `create_samples_from_segment` returns a pandas DataFrame
        containing information about the samples created from the input `drum_entry`.
        The DataFrame includes columns for 'style', 'audio_filename', and 'duration_in_seconds'
        of each sample.
        """

        soundfile_path = RAW_DATA_PATH.joinpath(drum_entry.audio_filename)
        soundsegment = AudioSegment.from_file(soundfile_path)
        sample_size = SAMPLE_INTERVAL * 1000 # sample size in milliseconds

        keys = list(drum_entry.index) # 'style', 'audio_filename'
        keys.append('duration_in_seconds') # adding duration in seconds of the sample
        # values = [[] for i in range(0, len(keys))]
        dict_info = {key: [] for key in keys}

        for i, chunk in enumerate(soundsegment[::sample_size]):
            drum_entry_sample = f'{soundfile_path.stem}_sample-{i+1}.wav'
            drum_entry_sample_path = SAMPLES_FOLDER_PATH / drum_entry.style / drum_entry_sample
            with drum_entry_sample_path.open('wb') as f:
                chunk.export(f, format='wav')
            for key in keys:
                if key == 'duration_in_seconds':
                    dict_info[key].append(chunk.duration_seconds)
                elif key == 'audio_filename':
                    dict_info[key].append(
                    Path(SAMPLES_FOLDER_PATH.stem) / drum_entry.style / drum_entry_sample)
                else:
                    dict_info[key].append(drum_entry[key])

        df = pd.DataFrame(dict_info)

        return df


    def create_audio_samples_from_df(self,
                            remove_previous:bool=False) -> pd.DataFrame:
        """
        The function `create_audio_samples_from_df` takes a DataFrame containing
        audio data, creates samples based on the data, and returns a new
        DataFrame with the information of the samples.

        :param remove_previous: The `remove_previous` parameter is a boolean flag that
        indicates whether any previously existing samples should be removed before
        creating new samples. If `remove_previous` is set to `True`, any existing
        samples will be deleted before creating new ones. If set to `False`, new samples
        will be created without removing, defaults to False
        :type remove_previous: bool (optional)

        :return: The function `create_audio_samples_from_df` returns a pandas DataFrame
        containing audio samples created from the input DataFrame `audio_df`.
        """
        # styles = list(audio_df['style'].unique())

        self.create_samples_folder(self.styles, remove_previous=remove_previous)
        audio_df = self.audio_raw_df[['style', 'audio_filename']].copy()
        samples_df = pd.DataFrame()

        print(Fore.GREEN + Style.BRIGHT + '\nCreating samples...\n' + Style.RESET_ALL)

        for index, row in tqdm(audio_df.iterrows(), total=audio_df.shape[0]):
            print(Fore.BLUE + Style.BRIGHT + f' Sampling audiofile # {index+1}... ' + Style.RESET_ALL)
            samples_df_ = self.create_samples_from_segment(row,
                                                SAMPLE_INTERVAL=SAMPLE_INTERVAL)
            samples_df = pd.concat([samples_df, samples_df_])

        print(Fore.BLUE + Style.BRIGHT + '\nDone!\n' + Style.RESET_ALL)

        self.samples_df = samples_df
