import pandas as pd

class PlayerRating:
    def __init__(self, standard_stats_path, passing_stats_path, goal_shot_stats_path, defensive_stats_path):
        self.standard_stats_path = standard_stats_path
        self.passing_stats_path = passing_stats_path
        self.goal_shot_stats_path = goal_shot_stats_path
        self.defensive_stats_path = defensive_stats_path
        self.df = None

    def load_and_merge_data(self):
        df = pd.read_csv(self.standard_stats_path, usecols=["Key", "League", "Team", "NonPenaltyGoalsPer90", "YelloCards", "ProgressiveCarries", "ProgressivePasses", "Min", "Goals", "Assists"])
        df1 = pd.read_csv(self.passing_stats_path, usecols=["Key", "Cmp%"])
        df2 = pd.read_csv(self.goal_shot_stats_path, usecols=["Key", "GCA90", "SCA90"])
        df3 = pd.read_csv(self.defensive_stats_path, usecols=["Key", "Total_Tackles", "Tackles_Won", "Interceptions", "Tackles_Def_3rd", "Tackles_mid_3rd"])

        df = df.drop_duplicates(subset="Key")
        df1 = df1.drop_duplicates(subset="Key")
        df2 = df2.drop_duplicates(subset="Key")
        df3 = df3.drop_duplicates(subset="Key")

        df["Season"] = df["Key"].str[:9]
        df1["Season"] = df1["Key"].str[:9]
        df2["Season"] = df2["Key"].str[:9]
        df3["Season"] = df3["Key"].str[:9]

        df_merged = df.merge(df1, on=["Key", "Season"], how="left")\
                      .merge(df2, on=["Key", "Season"], how="left")\
                      .merge(df3, on=["Key", "Season"], how="left")

        self.df = df_merged

    def clean_and_standardize(self):
        cols = ["NonPenaltyGoalsPer90", "YelloCards", "ProgressiveCarries", "ProgressivePasses", "Min", "Goals", "Assists", "Cmp%", "GCA90", "SCA90", "Total_Tackles", "Tackles_Won", "Interceptions", "Tackles_Def_3rd", "Tackles_mid_3rd"]
        for col in cols:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        self.df["Tackle%"] = self.df["Tackles_Won"] / self.df["Total_Tackles"]
        self.df["Goals_90"] = self.df["Goals"] / 90
        self.df["Assists_90"] = self.df["Assists"] / 90
        self.df["Player"] = self.df["Key"].str[10:]

        for col in ["NonPenaltyGoalsPer90", "YelloCards", "ProgressiveCarries", "ProgressivePasses", "Min", "Cmp%", "GCA90", "SCA90", "Total_Tackles", "Tackles_Won", "Interceptions", "Tackles_Def_3rd", "Tackles_mid_3rd", "Goals_90", "Assists_90", "Tackle%"]:
            self.df[f"{col}_z"] = (self.df[col] - self.df[col].mean()) / self.df[col].std()

    def calculate_player_ratings(self):
        self.df["PlayerRating"] = (
            0.2 * self.df["Goals_90_z"] +
            0.2 * self.df["Assists_90_z"] +
            0.14 * self.df["GCA90_z"] +
            0.1 * self.df["SCA90_z"] +
            0.06 * self.df["ProgressiveCarries_z"] +
            0.06 * self.df["ProgressivePasses_z"] +
            0.05 * self.df["Cmp%_z"] +
            0.03 * self.df["Min_z"] +
            0.02 * self.df["Tackle%_z"] +
            0.02 * self.df["Interceptions_z"] +
            0.01 * self.df["Tackles_Def_3rd"] +
            0.01 * self.df["Tackles_mid_3rd"] +
            (-0.02) * self.df["YelloCards"]
        )

        league_map = {
            'EPL': 1, 'LaLiga': 0.99, 'Bundesliga': 0.95, 'SerieA': 0.95,
            'Ligue1': 0.93, 'EreDivisie': 0.88, 'PrimeiraLiga': 0.88
        }

        self.df['LeagueRating'] = self.df['League'].map(league_map)

        min_rating = self.df["PlayerRating"].min()
        max_rating = self.df["PlayerRating"].max()

        self.df["PlayerRating_1_10"] = 0.9764 + 9 * (self.df["PlayerRating"] - min_rating) / (max_rating - min_rating)
        self.df["PlayerRatingActual"] = self.df["PlayerRating_1_10"] * self.df["LeagueRating"]

    def get_top_players(self, top_n=10):
        return self.df[["Player", "PlayerRatingActual", "Season"]].sort_values(by="PlayerRatingActual", ascending=False).dropna().head(top_n)
    
    def save_to_csv(self, output_path="Players.csv"):
        self.df["PlayerRatingActual"] = self.df["PlayerRatingActual"].round(2)

        self.df.to_csv(output_path, index=False)

if __name__ == "__main__":
    player_rating = PlayerRating(
        "./extracted_data/Cleaned_Standard_stats.csv", 
        "./extracted_data/Cleaned_Passing.csv",
        "./extracted_data/Cleaned_Goal_and_shot.csv",
        "./extracted_data/Cleaned_Defensive.csv"
    )

    player_rating.load_and_merge_data()
    player_rating.clean_and_standardize()
    player_rating.calculate_player_ratings()

    player_rating.save_to_csv("Players.csv")

    top_players = player_rating.get_top_players(20)
    print(top_players)
