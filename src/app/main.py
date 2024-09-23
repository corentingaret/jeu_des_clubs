import streamlit

import pandas
from datetime import datetime
import random

import helpers.preprocessing

MINIMUM_VALUE = 40  # minimum of player in millions
NUMBER_OF_ROUNDS = 5  # number of runs per user
POINTS_PERFECT = 3  # number of points you are given if perfect
PENALTY_HELP = 1  # number of points you lose if take help


def reset_player_state():
    streamlit.session_state["player_state"] = "new"
    streamlit.session_state["rounds_left"] -= 1
    streamlit.session_state["selected_player"] = ""  # Reset the selectbox choice


def display_clubs(year_help: bool) -> None:

    for i, club in enumerate(
        streamlit.session_state["player_df"].loc[0, "to_club_name"][-5:]
    ):

        if year_help is False:
            streamlit.markdown(f"{i+1}. {club}")
        else:
            streamlit.markdown(
                f"{i+1}. {club} - {streamlit.session_state['player_df'].loc[0, 'year'][i]}"
            )

    return


def get_new_player_info():
    streamlit.session_state["year_help"] = False
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
    return


def show_dashboard():
    streamlit.info(
        f"""
        Guess the player ⚽️
        Get the maximum points out of {NUMBER_OF_ROUNDS} rounds."""
    )

    column_dash = streamlit.columns(3)
    column_dash[0].metric(
        "Number of points", streamlit.session_state["user_total_points"]
    )
    column_dash[1].metric("Rounds left", streamlit.session_state["rounds_left"])
    return


def end_statement():
    streamlit.success("Thanks for playing, you scored a total of")
    column_dash = streamlit.columns(3)
    column_dash[0].metric("points", streamlit.session_state["user_total_points"])
    streamlit.markdown("(If you want to play again, just reload the page)")
    return


streamlit.title("Jeu des clubs 🎊")

# INIT SESSION STATE
if "player_state" not in streamlit.session_state:
    streamlit.session_state["player_state"] = "new"

if "year_help" not in streamlit.session_state:
    streamlit.session_state["year_help"] = False

if "user_total_points" not in streamlit.session_state:
    streamlit.session_state["user_total_points"] = 0

if "rounds_left" not in streamlit.session_state:
    streamlit.session_state["rounds_left"] = NUMBER_OF_ROUNDS

if streamlit.session_state["player_state"] == "new":
    streamlit.session_state["round_points"] = POINTS_PERFECT

if streamlit.session_state["player_state"] == "new":
    streamlit.session_state["show_solution"] = False

if streamlit.session_state["player_state"] == "new":
    streamlit.session_state["is_correct"] = False

if streamlit.session_state["player_state"] == "new":
    streamlit.session_state["is_wrong"] = False

if "selected_player" not in streamlit.session_state:
    streamlit.session_state["selected_player"] = ""

# GET DATA
df = pandas.read_csv("data/archive/transfers.csv")
clubs = pandas.read_csv("data/archive/clubs.csv")

# CHECK IF FINISHED
if streamlit.session_state["rounds_left"] == 0:
    end_statement()

else:
    # DASHBOARD
    show_dashboard()

    # PREPROCESSING
    df = helpers.preprocessing.complete_preprocessing(df=df, clubs=clubs)
    grouped, players_id, players_names = helpers.preprocessing.prepare_data(
        df=df, minimum_value=MINIMUM_VALUE
    )

    # GET NEW PLAYER INFO
    if streamlit.session_state["player_state"] == "new":
        get_new_player_info()

    # DISPLAY CLUBS
    display_clubs(year_help=streamlit.session_state["year_help"])

    choice = streamlit.selectbox(
        label="Player", options=[""] + players_names, index=0, key="selected_player"
    )

    # BUTTONS
    columns = streamlit.columns(4)
    if columns[0].button(f'Submit ({streamlit.session_state["round_points"]} pts)'):
        if choice == streamlit.session_state["player_name"]:
            streamlit.success("Correct! 🎉")
            streamlit.session_state["is_correct"] = True
            streamlit.session_state["user_total_points"] += streamlit.session_state[
                "round_points"
            ]
            streamlit.experimental_rerun()

        if choice != "" and choice != streamlit.session_state["player_name"]:
            streamlit.session_state["is_wrong"] = True

    if streamlit.session_state["is_correct"]:
        streamlit.success("Correct! 🎉")

    if streamlit.session_state["is_wrong"]:
        streamlit.error("Wrong! ❌")

    if columns[1].button(f"Help me! (-{PENALTY_HELP} pts)"):
        streamlit.session_state["year_help"] = True
        streamlit.session_state["round_points"] = max(
            streamlit.session_state["round_points"] - PENALTY_HELP, 0
        )
        streamlit.experimental_rerun()

    # SOLUTION
    if streamlit.button("Give me the solution (0 pts)"):
        streamlit.session_state["show_solution"] = True
        streamlit.session_state["round_points"] = 0
        streamlit.experimental_rerun()

    if streamlit.session_state["show_solution"]:
        streamlit.warning(streamlit.session_state["player_name"])

    # CHANGE PLAYER
    streamlit.divider()

    if streamlit.button("Next round", on_click=reset_player_state):
        pass

    if streamlit.session_state["player_state"] == "new":
        pass

    if streamlit.session_state["year_help"] == False:
        pass
