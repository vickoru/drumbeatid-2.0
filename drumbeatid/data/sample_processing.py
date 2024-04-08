import numpy as np
import pandas as pd

from pathlib import Path
import shutil

from pydub import AudioSegment

from colorama import Fore, Style

from drumbeatid.params import *


def create_samples_folder(styles:list,
                          remove_previous:bool=False,
                          gdrive='/content/drive') -> str:
    '''
    Create folder structure to create the samples using pydub AudioSegment.
    If overwrite=True (default=False), the folder is removed and created again.
    '''

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
            print(f'The folder for the style {style} already exists. Please verify that the sample duration you have chosen has not already been processed.')
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
    '''
    '''

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


def processing_drummers(dataframe:pd.DataFrame) -> pd.DataFrame:
    '''
    Process the original infocsv to build the input DataFrame for the model
    with the necessary columns.
    '''
    df_drummers = dataframe.drop(columns=['drummer', 'id', 'session', 'split', 'midi_filename'])
    df_drummers = df_drummers.dropna()
    df_drummers = df_drummers[df_drummers['beat_type'] == 'beat']
    style_list = df_drummers['style'].apply(
        lambda x: x.split('/')[0]).to_list()
    df_drummers = df_drummers.drop(columns='style')
    df_drummers.loc[:, 'style'] = style_list

    return df_drummers

def count_sequences(dataframe:pd.DataFrame, seq:int=10) -> pd.DataFrame:
    '''
    Count how many samples would be possible to generate given the
    original wav files if they were split into non-overlapping samples
    of seq seconds duration
    '''
    total_seconds = dataframe[['style', 'duration']].groupby(
        by='style').sum().sort_values(by='duration')
    total_seconds.loc[:, 'number_sequences'] = \
        total_seconds['duration'].apply(
            lambda x: int(x/seq))

    return total_seconds
