import pandas
from datetime import datetime


def is_not_after_today(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
    current_date = datetime.now()
    input_date = datetime.strptime(date_str, date_format)
    return input_date <= current_date


def club_preprocessing(club: str) -> str:

    na = "na"

    if club == "Without Club":
        return na

    if " U1" in club or " U2" in club:
        return na

    if " Sub-1" in club:
        return na

    if club.endswith(" B") or club.endswith(" Yth."):
        return na

    if club.endswith(" II") or club.endswith(" Youth"):
        return na

    return club


def complete_preprocessing(
    df: pandas.DataFrame, clubs: pandas.DataFrame
) -> pandas.DataFrame:

    df = df.sort_values(by=["player_id", "transfer_date"], ascending=True)

    df = df.merge(clubs, how="inner", left_on="to_club_id", right_on="club_id")

    df["fg_valid_transfer_date"] = df["transfer_date"].apply(is_not_after_today)
    df = df.loc[df["fg_valid_transfer_date"] == True].copy()

    df["preprocessed_to_club_name"] = df["to_club_name"].apply(club_preprocessing)
    df["market_value_in_eur"] = df["market_value_in_eur"] / 1_000_000
    df = df.loc[df["preprocessed_to_club_name"] != "na"].copy()

    return df


def prepare_data(df: pandas.DataFrame):

    grouped = (
        df.groupby(["player_id", "player_name"])
        .agg({"to_club_name": list, "market_value_in_eur": "max"})
        .reset_index()
    )

    grouped = grouped.loc[grouped["market_value_in_eur"] >= 20].copy()

    players_id = grouped["player_id"].tolist()
    players_names = grouped["player_name"].tolist()

    return grouped, players_id, players_names
