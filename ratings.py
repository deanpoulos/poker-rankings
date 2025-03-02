from datetime import datetime

import pandas as pd
import trueskill


def calculate_trueskill_ratings(df: pd.DataFrame) -> pd.DataFrame:
    # Initialize TrueSkill environment
    env = trueskill.TrueSkill()
    ratings = {player: env.create_rating() for player in df.columns[1:]}

    # Process game results row by row
    for _, row in df.iterrows():
        scores = row.iloc[1:].dropna() # Exclude the 'Date' column
        print(row.iloc[1:].dropna().sort_values())
        players = list(scores.index)
        rankings = scores.rank(method="dense", ascending=True).astype(int)

        # Sort players by their ranking
        sorted_players = [p for _, p in sorted(zip(rankings, players))]

        # Update ratings
        rated_players = [ratings[p] for p in sorted_players]
        new_ratings = env.rate([(r,) for r in rated_players])

        # Store updated ratings
        for p, (new_rating,) in zip(sorted_players, new_ratings):
            ratings[p] = new_rating

    # Convert ratings to a DataFrame
    rating_df = pd.DataFrame({
        "Player": list(ratings.keys()),
        "Mu": [r.mu for r in ratings.values()],  # Skill estimate
        "Sigma": [r.sigma for r in ratings.values()],  # Uncertainty
        "TrueSkill": [r.mu - 3 * r.sigma for r in ratings.values()]  # Conservative rating
    })

    return rating_df


def filter_by_last_played(df: pd.DataFrame, rating_df: pd.DataFrame, threshold_date: datetime) -> pd.DataFrame:
    # Example DataFrame df with a Date column (assume your table already includes the 'Date' column)
    # Rename 'GAMES' to 'Date' and make sure it's a datetime column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Filter the DataFrame for games played in the past year
    df_recent = df[df["Date"] >= threshold_date]

    # Now, filter out players who have not played in the past year
    # Create a set of players who have participated in games within the last year
    players_played_recently = df_recent.dropna(axis=1, how="all").columns[1:]

    # Filter ranking_df based on this list of players
    ranking_df_filtered = rating_df[rating_df["Player"].isin(players_played_recently)]

    return ranking_df_filtered
