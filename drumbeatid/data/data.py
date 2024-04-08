import pandas as pd
from pathlib import Path

from colorama import Fore, Style

from drumbeatid.data.sample_processing import create_samples_folder, create_samples_from_segment
from drumbeatid.params import *


def create_audio_samples_from_df(audio_df:pd.DataFrame,
                        remove_previous:bool=False) -> pd.DataFrame:
    '''
    '''

    styles = list(audio_df['style'].unique())

    create_samples_folder(styles, remove_previous=remove_previous)

    samples_df = pd.DataFrame()

    print(Fore.GREEN + Style.BRIGHT + '\nCreating samples...\n' + Style.RESET_ALL)

    for index, row in audio_df.iterrows():
        samples_df_ = create_samples_from_segment(row, SAMPLE_INTERVAL=SAMPLE_INTERVAL)
        samples_df = pd.concat([samples_df, samples_df_])

    print(Fore.BLUE + Style.BRIGHT + '\nDone!\n' + Style.RESET_ALL)

    return samples_df


def main(remove_previous=False):
    '''
    '''
    audio_df = pd.read_csv(RAW_DATA_PATH / '..' / 'info_test.csv')
    samples_df = create_audio_samples_from_df(
        audio_df=audio_df, remove_previous=remove_previous)
    df_csv_path = SAMPLES_FOLDER_PATH.parent / (SAMPLES_FOLDER_PATH.stem + '.csv')
    samples_df.to_csv(df_csv_path, index=False)

    return None




# def create_audio_samples(styles:list,
#                          path_audio:pathlib.PosixPath=PATH_RAW_DATA,
#                          audio_type:str='wav',
#                         remove_previous:bool=False) -> None:
#     '''
#     '''

#     create_samples_folder(styles, remove_previous=remove_previous)


#     audio_files = [path.resolve() for path in
#                    list(PATH_RAW_DATA.iterdir())
#                    if path.suffix == f'.{audio_type}']

#     print(Fore.GREEN + Style.BRIGHT + '\nCreating samples...\n' + Style.RESET_ALL)

#     for index, row in audio_df.iterrows():
#         samples_df_ = create_samples_from_segment(row, SAMPLE_INTERVAL=SAMPLE_INTERVAL)
#         samples_df = pd.concat([samples_df, samples_df_])

#     print(Fore.BLUE + Style.BRIGHT + '\nDone!\n' + Style.RESET_ALL)

#     return samples_df


if __name__ == '__main__':
    main(remove_previous=False)
