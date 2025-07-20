from datetime import datetime, timedelta

from cleaning import *
from ratings import calculate_trueskill_ratings, filter_by_last_played

df = pd.read_csv("data/2025-07-20.csv", skiprows=1)

df = drop_non_tournament_rows(df)
df = drop_profit_columns(df)
df = drop_non_player_columns(df)

df = recast_table_values_from_strings(df)

print(df)

rating_df = calculate_trueskill_ratings(df)
rating_df = filter_by_last_played(df, rating_df, threshold_date=datetime.now() - timedelta(days=365))

rating_df = rating_df.sort_values(by="TrueSkill", ascending=False).reset_index(drop=True)

print(rating_df)
