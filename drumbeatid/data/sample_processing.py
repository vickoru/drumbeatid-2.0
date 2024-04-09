import numpy as np
import pandas as pd

from pathlib import Path
import shutil

from pydub import AudioSegment

from colorama import Fore, Style
from tqdm import tqdm

from drumbeatid.params import *


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

    return None



def create_samples_from_segment(drum_entry:pd.Series,
                                SAMPLE_INTERVAL:int=SAMPLE_INTERVAL) -> pd.DataFrame:
    """
    The function `create_samples_from_segment` generates samples from a given audio
    segment and returns a DataFrame with information about each generated sample.

    :param drum_entry: The `drum_entry` parameter is a pandas Series containing
    information about a specific drum entry. Each entry must include details such as time
    signature, BPM, style, audio filename as columns. This function takes this drum entry
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
    The DataFrame includes columns for 'time_signature', 'bpm', 'style',
    'audio_filename', and 'duration_in_seconds' of each sample.
    """

    soundfile_path = RAW_DATA_PATH.joinpath(drum_entry.audio_filename)
    soundsegment = AudioSegment.from_file(soundfile_path)
    sample_size = SAMPLE_INTERVAL * 1000 # sample size in milliseconds

    keys = list(drum_entry.index) # 'time_signature', 'bpm', 'style', 'audio_filename'
    keys.append('duration_in_seconds') # adding duration in seconds of the sample
    values = [[] for i in range(0, len(keys))]

    for i, chunk in enumerate(soundsegment[::sample_size]):
        drum_entry_sample = f'{soundfile_path.stem}_sample-{i+1}.wav'
        drum_entry_sample_path = SAMPLES_FOLDER_PATH / drum_entry.style / drum_entry_sample
        with drum_entry_sample_path.open('wb') as f:
            chunk.export(f, format='wav')
        values[0].append(drum_entry.time_signature)
        values[1].append(drum_entry.bpm)
        values[2].append(drum_entry.style)
        values[3].append(drum_entry_sample)
        values[4].append(chunk.duration_seconds)

    df = pd.DataFrame(dict(zip(keys, values)))

    return df


def create_audio_samples_from_df(audio_df:pd.DataFrame,
                            remove_previous:bool=False) -> pd.DataFrame:
    """
    The function `create_audio_samples_from_df` takes a DataFrame containing
    audio data, creates samples based on the data, and returns a new
    DataFrame with the information of the samples.

    :param audio_df: The `audio_df` parameter is a pandas DataFrame containing
    information about audio files. The DataFrame has a column named 'style'
    which contains different styles of audio files. The function
    `create_audio_samples_from_df` is designed to create audio samples from the
    data in this DataFrame.
    :type audio_df: pd.DataFrame

    :param remove_previous: The `remove_previous` parameter is a boolean flag that
    indicates whether any previously existing samples should be removed before
    creating new samples. If `remove_previous` is set to `True`, any existing
    samples will be deleted before creating new ones. If set to `False`, new samples
    will be created without removing, defaults to False
    :type remove_previous: bool (optional)

    :return: The function `create_audio_samples_from_df` returns a pandas DataFrame
    containing audio samples created from the input DataFrame `audio_df`.
    """
    styles = list(audio_df['style'].unique())

    create_samples_folder(styles, remove_previous=remove_previous)

    samples_df = pd.DataFrame()

    print(Fore.GREEN + Style.BRIGHT + '\nCreating samples...\n' + Style.RESET_ALL)

    for index, row in tqdm(audio_df.iterrows(), total=audio_df.shape[0]):
        print(Fore.BLUE + Style.BRIGHT + f' Sampling audiofile # {index+1}... ' + Style.RESET_ALL)
        samples_df_ = create_samples_from_segment(row, SAMPLE_INTERVAL=SAMPLE_INTERVAL)
        samples_df = pd.concat([samples_df, samples_df_])

    print(Fore.BLUE + Style.BRIGHT + '\nDone!\n' + Style.RESET_ALL)

    return samples_df


def processing_drummers(dataframe:pd.DataFrame) -> pd.DataFrame:
    """
     Process the original infocsv to build the input DataFrame for the model
    with the necessary columns.
    The function `processing_drummers` processes a DataFrame (infocsv) by
    dropping specific columns, removing rows with missing values, filtering rows
    by `beat_type` == `beat` instead of `fill` beata condition,
    and processing the style of drumming.

    :param dataframe: The function `processing_drummers` takes a pandas DataFrame as
    input and performs some data processing steps on it. It drops certain columns
    ('drummer', 'id', 'session', 'split', 'midi_filename'), removes any rows with
    missing values, filters rows where 'beat_type' is 'beat'.
    :type dataframe: pd.DataFrame

    :return: The function `processing_drummers returns the modified DataFrame
    with a new 'style' column that defines the drumming style.
    """

    df_drummers = dataframe.drop(columns=['drummer', 'id',
                                          'session', 'split', 'midi_filename'])
    df_drummers = df_drummers.dropna()
    df_drummers = df_drummers[df_drummers['beat_type'] == 'beat']
    style_list = df_drummers['style'].apply(
        lambda x: x.split('/')[0]).to_list()
    df_drummers = df_drummers.drop(columns='style')
    df_drummers.loc[:, 'style'] = style_list

    return df_drummers


def count_sequences(dataframe:pd.DataFrame, seq:int=10) -> pd.DataFrame:
    """
    This function calculates the number of non-overlapping samples that can be
    generated from original audio files based on their duration and a specified
    sequence length.

    :param dataframe: A pandas DataFrame containing information about the original
    wav files, including the style of the audio and the duration of each file. The
    DataFrame should have columns 'style' and 'duration'.
    :type dataframe: pd.DataFrame

    :param seq: The `seq` parameter in the `count_sequences` function represents the
    duration in seconds for each non-overlapping sample that the original wav files
    would be split into. This parameter is used to calculate how many samples would
    be possible to generate from the original wav files based on the specified
    duration for each sample, defaults to 10.
    :type seq: int (optional)

    :return: A DataFrame is being returned with the total duration of audio samples
    for each style in the input DataFrame, along with the corresponding number of
    non-overlapping sequences that could be generated from each style's total
    duration by splitting it into segments of `seq` seconds.
    """

    total_seconds = dataframe[['style', 'duration']].groupby(
        by='style').sum().sort_values(by='duration')
    total_seconds.loc[:, 'number_sequences'] = \
        total_seconds['duration'].apply(
            lambda x: int(x/seq))

    return total_seconds
