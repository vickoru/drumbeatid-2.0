import pandas as pd

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
