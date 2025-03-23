import pandas as pd

class PlayerRating:
    def __init__(self, standard_stats_path, passing_stats_path, goal_shot_stats_path, defensive_stats_path):
        # Initiera filvägarna för alla dataset
        self.standard_stats_path = standard_stats_path
        self.passing_stats_path = passing_stats_path
        self.goal_shot_stats_path = goal_shot_stats_path
        self.defensive_stats_path = defensive_stats_path
        self.df = None
        
    def load_and_merge_data(self):
        # Läs in alla dataset
        df = pd.read_csv(self.standard_stats_path, usecols=["Key", "NonPenaltyGoalsPer90", "YelloCards", "ProgressiveCarries", "ProgressivePasses", "Min", "Goals", "Assists"])
        df1 = pd.read_csv(self.passing_stats_path, usecols=["Key", "Cmp%"])
        df2 = pd.read_csv(self.goal_shot_stats_path, usecols=["Key", "GCA90", "SCA90"])
        df3 = pd.read_csv(self.defensive_stats_path, usecols=["Key", "Total_Tackles", "Tackles_Won"])

        # Ta bort duplicerade 'Key' värden
        df = df.drop_duplicates(subset="Key")
        df1 = df1.drop_duplicates(subset="Key")
        df2 = df2.drop_duplicates(subset="Key")
        df3 = df3.drop_duplicates(subset="Key")

        # Lägg till season kolumn
        df["Season"] = df["Key"].str[:9]
        df1["Season"] = df1["Key"].str[:9]
        df2["Season"] = df2["Key"].str[:9]
        df3["Season"] = df3["Key"].str[:9]

        # Mergar alla datasets
        df_merged1 = pd.merge(df, df1, on=["Key", "Season"], how="left")
        df_merged2 = pd.merge(df_merged1, df2, on=["Key", "Season"], how="left")
        df_merged3 = pd.merge(df_merged2, df3, on=["Key", "Season"], how="left")
        
        self.df = df_merged3

    def clean_and_standardize(self):
        # Konvertera kolumner till numeriska värden
        cols = ["NonPenaltyGoalsPer90", "YelloCards", "ProgressiveCarries", "ProgressivePasses", "Min", "Goals", "Assists", "Cmp%", "GCA90", "SCA90", "Total_Tackles", "Tackles_Won"]
        for col in cols:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # Skapa nya kolumner
        self.df["Tackle%"] = self.df["Tackles_Won"] / self.df["Total_Tackles"]
        self.df["Goals_90"] = self.df["Goals"] / 90
        self.df["Assists_90"] = self.df["Assists"] / 90
        self.df["Player"] = self.df["Key"].str[10:]
        
        # Z-standardisering för varje relevant kolumn
        for col in ["Goals", "Assists", "YelloCards", "ProgressiveCarries", "ProgressivePasses", "NonPenaltyGoalsPer90", "Cmp%", "SCA90", "GCA90", "Tackle%", "Goals_90", "Assists_90"]:
            self.df[f"{col}_z"] = (self.df[col] - self.df[col].mean()) / self.df[col].std()

    def calculate_player_ratings(self):
        # Beräkna spelarens betyg med viktade z-scores
        self.df["PlayerRating"] = (
            0.1 * self.df["ProgressiveCarries_z"] + 
            0.1 * self.df["ProgressivePasses_z"] + 
            0.1 * self.df["NonPenaltyGoalsPer90_z"] + 
            0.15 * self.df["Cmp%_z"] + 
            0.05 * self.df["SCA90_z"] + 
            0.05 * self.df["GCA90_z"] + 
            0.10 * self.df["Tackle%_z"] + 
            0.2 * self.df["Goals_90_z"] + 
            0.15 * self.df["Assists_90_z"] +
            (-0.05) * self.df["YelloCards_z"]
        )

        min_rating = self.df["PlayerRating"].min()
        max_rating = self.df["PlayerRating"].max()

        self.df["PlayerRating_1_10"] = 0.9764 + 9 * (self.df["PlayerRating"] - min_rating) / (max_rating - min_rating)

    def get_top_players(self, top_n=10):
        # Hämta de bästa spelarna
        return self.df[["Player", "PlayerRating_1_10", "Season"]].sort_values(by="PlayerRating_1_10", ascending=False).head(top_n)


if __name__ == "__main__":
    # Skapa en instans av klassen och använd metoderna
    player_rating = PlayerRating(
        "./extracted_data/Cleaned_Standard_stats.csv", 
        "./extracted_data/Cleaned_Passing.csv",
        "./extracted_data/Cleaned_Goal_and_shot.csv",
        "./extracted_Data/Cleaned_Defensive.csv"
    )
    
    player_rating.load_and_merge_data()
    player_rating.clean_and_standardize()
    player_rating.calculate_player_ratings()
    
    top_players = player_rating.get_top_players()
    print(top_players)