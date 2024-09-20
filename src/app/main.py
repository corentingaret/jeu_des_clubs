
import streamlit

import pandas
from datetime import datetime
import random

def is_not_after_today(date_str: str, date_format: str ='%Y-%m-%d') -> bool:
    current_date = datetime.now()
    input_date = datetime.strptime(date_str, date_format)
    return input_date <= current_date


def club_preprocessing(club: str) -> str:
    
    na = 'na'
    
    if club == 'Without Club':
        return na
    
    if ' U1' in club or ' U2' in club:
        return na
    
    if ' Sub-1' in club:
        return na
    
    if club.endswith(' B') or club.endswith(' Yth.'):
        return na
    
    if club.endswith(' II') or club.endswith(' Youth'):
        return na
        
    return club


def complete_preprocessing(df: pandas.DataFrame) -> pandas.DataFrame:
    
    df = df.sort_values(by=['player_id', 'transfer_date'], ascending=True)

    df["fg_valid_transfer_date"] = df["transfer_date"].apply(is_not_after_today)
    df = df.loc[df['fg_valid_transfer_date'] == True].copy()

    df['preprocessed_to_club_name'] = df['to_club_name'].apply(club_preprocessing)
    df['market_value_in_eur'] = df['market_value_in_eur'] / 1_000_000
    df = df.loc[df['preprocessed_to_club_name'] != 'na'].copy()
    
    return df


def prepare_data(df: pandas.DataFrame):
    
    grouped = df.groupby(['player_id', 'player_name']).agg({
        'to_club_name': list,
        'market_value_in_eur': 'max'
    }).reset_index()

    grouped = grouped.loc[grouped['market_value_in_eur'] >= 20].copy()

    players_id = grouped['player_id'].tolist()
    players_names = grouped['player_name'].tolist()
    
    return grouped, players_id, players_names


streamlit.title("Jeu des clubs 🎊")

# Init session state
if 'player_state' not in streamlit.session_state:
    streamlit.session_state['player_state'] = 'new'
    
df = pandas.read_csv("data/archive/transfers.csv")

streamlit.info("Guess the player ⚽️")

# PREPROCESSING
df = complete_preprocessing(df)
grouped, players_id, players_names = prepare_data(df)

# GET NEW PLAYER INFO
if streamlit.session_state['player_state'] == 'new':
    
    streamlit.session_state['player_id'] = random.choice(players_id)
    streamlit.session_state['player_df'] = grouped.loc[grouped['player_id'] == streamlit.session_state['player_id']].reset_index().copy()
    streamlit.session_state['player_name'] = streamlit.session_state['player_df'].loc[0, 'player_name']
    
    streamlit.session_state['player_state'] = 'old'

for i, club in enumerate(streamlit.session_state['player_df'].loc[0, 'to_club_name']):
    streamlit.markdown(f'{i}. {club}')
    
choice = streamlit.selectbox(label="Player", options=[''] + players_names, index=0)

if choice == streamlit.session_state['player_name']:
    streamlit.success('Correct! 🎉')
    
if choice != '' and choice != streamlit.session_state['player_name']:
    streamlit.error('Wrong! ❌')

def reset_player_state():
    streamlit.session_state['player_state'] = 'new'

if streamlit.button('Give me another player', on_click=reset_player_state):
    pass

if streamlit.session_state['player_state'] == 'new':
    pass
