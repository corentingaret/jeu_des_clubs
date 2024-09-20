import streamlit

import pandas
from datetime import datetime
import random

import helpers.preprocessing


def reset_player_state():
    streamlit.session_state["player_state"] = "new"


streamlit.title("Jeu des clubs 🎊")

# Init session state
if "player_state" not in streamlit.session_state:
    streamlit.session_state["player_state"] = "new"

df = pandas.read_csv("data/archive/transfers.csv")
clubs = pandas.read_csv("data/archive/clubs.csv")

streamlit.info("Guess the player ⚽️")

# PREPROCESSING
df = helpers.preprocessing.complete_preprocessing(df=df, clubs=clubs)
grouped, players_id, players_names = helpers.preprocessing.prepare_data(df)

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
for i, club in enumerate(
    streamlit.session_state["player_df"].loc[0, "to_club_name"][-5:]
):
    streamlit.markdown(f"{i+1}. {club}")

choice = streamlit.selectbox(label="Player", options=[""] + players_names, index=0)

columns = streamlit.columns(4)

if columns[0].button("Submit"):
    if choice == streamlit.session_state["player_name"]:
        streamlit.success("Correct! 🎉")

    if choice != "" and choice != streamlit.session_state["player_name"]:
        streamlit.error("Wrong! ❌")

if columns[1].button("Give me the solution"):
    streamlit.warning(streamlit.session_state["player_name"])

streamlit.divider()

if streamlit.button("Give me another player", on_click=reset_player_state):
    pass

if streamlit.session_state["player_state"] == "new":
    pass
