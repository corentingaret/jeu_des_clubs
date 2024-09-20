import streamlit

import pandas
from datetime import datetime
import random

import helpers.preprocessing

MINIMUM_VALUE = 40


def reset_player_state():
    streamlit.session_state["player_state"] = "new"


def display_clubs(year_help: bool) -> None:

    for i, club in enumerate(
        streamlit.session_state["player_df"].loc[0, "to_club_name"][-5:]
    ):

        if year_help:
            streamlit.markdown(f"{i+1}. {club}")
        else:
            streamlit.markdown(
                f"{i+1}. {club} - {streamlit.session_state['player_df'].loc[0, 'year'][i]}"
            )

    return


streamlit.title("Jeu des clubs 🎊")

# INIT SESSION STATE
if "player_state" not in streamlit.session_state:
    streamlit.session_state["player_state"] = "new"

if "year_help" not in streamlit.session_state:
    streamlit.session_state["year_help"] = False

df = pandas.read_csv("data/archive/transfers.csv")
clubs = pandas.read_csv("data/archive/clubs.csv")

streamlit.info("Guess the player ⚽️")

# PREPROCESSING
df = helpers.preprocessing.complete_preprocessing(df=df, clubs=clubs)
grouped, players_id, players_names = helpers.preprocessing.prepare_data(
    df=df, minimum_value=MINIMUM_VALUE
)

# GET NEW PLAYER INFO
if streamlit.session_state["player_state"] == "new":

    streamlit.session_state["player_id"] = random.choice(players_id)
    streamlit.session_state["player_df"] = (
        grouped.loc[grouped["player_id"] == streamlit.session_state["player_id"]]
        .reset_index()
        .copy()
    )
    streamlit.session_state["player_name"] = streamlit.session_state["player_df"].loc[
        0, "player_name"
    ]

    streamlit.session_state["player_state"] = "old"

# DISPLAY CLUBS
display_clubs(year_help=streamlit.session_state["year_help"])

choice = streamlit.selectbox(label="Player", options=[""] + players_names, index=0)

# BUTTONS
columns = streamlit.columns(4)
if columns[0].button("Submit"):
    if choice == streamlit.session_state["player_name"]:
        streamlit.success("Correct! 🎉")

    if choice != "" and choice != streamlit.session_state["player_name"]:
        streamlit.error("Wrong! ❌")

if columns[1].button("Help me!"):
    streamlit.session_state["year_help"] = True

# SOLUTION
if streamlit.button("Give me the solution"):
    streamlit.warning(streamlit.session_state["player_name"])

# CHANGE PLAYER
streamlit.divider()

if streamlit.button("Give me another player", on_click=reset_player_state):
    pass

if streamlit.session_state["player_state"] == "new":
    pass

if streamlit.session_state["year_help"] == False:
    pass
