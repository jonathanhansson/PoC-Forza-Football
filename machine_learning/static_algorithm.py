import pandas as pd
import numpy as np

class PlayerRating:
    position_weights = {
        "GK": {  # Målvakt
            "Save%": 0.7,            # Ökad vikt för räddningar
            "GA90_z": -0.3,          # Straff mot per 90 minuter
            "CS%_z": 0.5,            # Clean sheets
            "W_z": 0.1               # Bidrag till lagets vinster
        },
        "DF": {  # Försvarare
            "Tackle%_z": 0.15,         # Tacklingsförmåga
            "Interceptions_90_z": 0.15,# Avlyssningar per 90 minuter
            "Tackles_Def_3rd_90_z": 0.15, # Tacklingsinsatser i den defensiva zonen
            "Shots_Blocked_90_z": 0.1,  # Blockerade skott per 90 minuter
            "ProgressivePasses_90_z": 0.2, # Effektiva passningar som bidrar offensivt
            "GoalsPer90_z": 0.25,      # Mål per 90 (värdefullt vid omställningar)
            "YelloCards_90_z": -0.20   # Negativ påverkan från gula kort
        },
        "MF": {  # Mittfältare
            "Cmp%_z": 0.15,           # Passningsprocent
            "PrgDist_90_z": 0.15,      # Progressiv distans per 90
            "GCA90_z": 0.20,           # Målchansskapande
            "ProgressiveCarries_90_z": 0.15,  # Framåtdrivande löpningar
            "ProgressivePasses_90_z": 0.15,   # Progressiva passningar
            "Tackle%_z": 0.10,         # Tacklingsprocent
            "GoalsPer90_z": 0.05,      # Mål per 90 (mindre vikt)
            "AssistPer90_z": 0.05      # Assist per 90 (mindre vikt)
        },
        "FW": {  # Anfallare
            "NonPenaltyGoalsPer90_z": 0.30, # Mål per 90 utan straff
            "GCA90_z": 0.30,                # Målchansskapande
            "ProgressiveCarries_90_z": 0.2,
            "GoalsandAssistPer90_z": 0.10,  # Kombinerat mål- och assistbidrag
            "GoalsPerShotOnTarget_z": 0.10  # Skottprecision
        }
    }


    league_ratings = {
    "Premier League": 1,
    "La Liga": 1,
    "Serie A": 0.96,
    "Bundesliga": 0.96,
    "Ligue 1": 0.93,
    "EreDivisie": 0.90,
    "PrimeiraLiga": 0.92
    }   
        
    
    def __init__(self, standard_stats_path, passing_stats_path, goal_shot_stats_path, defensive_stats_path, goalkeeping_stats_path, shooting_stats_path):
        self.standard_stats_path = standard_stats_path
        self.passing_stats_path = passing_stats_path
        self.goal_shot_stats_path = goal_shot_stats_path
        self.defensive_stats_path = defensive_stats_path
        self.goalkeeping_stats_path = goalkeeping_stats_path
        self.shooting_stats_path = shooting_stats_path
        self.df = None

    def load_and_merge_data(self):
        df = pd.read_csv(self.standard_stats_path, usecols=["Key", "Min", "League", "Team", "Pos", "GoalsPer90", "YelloCards", "AssistPer90", "NonPenaltyGoalsPer90", "GoalsandAssistPer90", "ProgressiveCarries", "ProgressivePasses"])
        df1 = pd.read_csv(self.passing_stats_path, usecols=["Key", "Cmp%", "PrgDist"])
        df2 = pd.read_csv(self.goal_shot_stats_path, usecols=["Key", "GCA90", "SCA90"])
        df3 = pd.read_csv(self.defensive_stats_path, usecols=["Key", "Total_Tackles", "Tackles_Won", "Interceptions", "Tackles_Def_3rd", "Tackles_mid_3rd", "Shots_Blocked"])
        df4 = pd.read_csv(self.goalkeeping_stats_path, usecols=["Key", "Save%", "GA90", "CS%", "W"])
        df5 = pd.read_csv(self.shooting_stats_path, usecols=["Key", "GoalsPerShotOnTarget"])

        df = df.drop_duplicates(subset="Key")
        df1 = df1.drop_duplicates(subset="Key")
        df2 = df2.drop_duplicates(subset="Key")
        df3 = df3.drop_duplicates(subset="Key")
        df4 = df4.drop_duplicates(subset="Key")
        df5 = df5.drop_duplicates(subset="Key")

        df["Season"] = df["Key"].str[:9]
        df1["Season"] = df1["Key"].str[:9]
        df2["Season"] = df2["Key"].str[:9]
        df3["Season"] = df3["Key"].str[:9]
        df4["Season"] = df4["Key"].str[:9]
        df5["Season"] = df5["Key"].str[:9]

        df_merged = df.merge(df1, on=["Key", "Season"], how="left")\
                      .merge(df2, on=["Key", "Season"], how="left")\
                      .merge(df3, on=["Key", "Season"], how="left")\
                      .merge(df4, on=["Key", "Season"], how="left")\
                      .merge(df5, on=["Key", "Season"], how="left")
        
        df_merged["Min"] = pd.to_numeric(df_merged["Min"], errors="coerce")
        
        self.df = df_merged[df_merged["Min"] >= 1000]

    def clean_and_standardize(self):
        cols = ["GoalsPer90", "YelloCards", "AssistPer90", "NonPenaltyGoalsPer90", "GoalsandAssistPer90", "ProgressiveCarries", "ProgressivePasses", "Cmp%", "PrgDist", "GCA90", "SCA90", "Total_Tackles", "Tackles_Won", "Interceptions", "Tackles_Def_3rd", "Tackles_mid_3rd", "Shots_Blocked", "Save%", "GA90", "CS%", "W", "GoalsPerShotOnTarget"]
        for col in cols:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        self.df["YelloCards_90"] = self.df["YelloCards"] / 90
        self.df["ProgressiveCarries_90"] = self.df["ProgressiveCarries"] / 90
        self.df["ProgressivePasses_90"] = self.df["ProgressivePasses"] / 90
        self.df["PrgDist_90"] = self.df["PrgDist"] / 90
        self.df.loc[self.df["Total_Tackles"] >= 1, "Tackle%"] = self.df["Tackles_Won"] / self.df["Total_Tackles"]
        self.df["Interceptions_90"] = self.df["Interceptions"] / 90
        self.df["Tackles_Def_3rd_90"] = self.df["Tackles_Def_3rd"] / 90
        self.df["Tackles_Mid_3rd_90"] = self.df["Tackles_mid_3rd"] / 90
        self.df["Shots_Blocked_90"] = self.df["Shots_Blocked"] / 90
        self.df["Pos"] = self.df["Pos"].str.split(",").str[0]

        self.df["Player"] = self.df["Key"].str[10:]

        for position in ["GK", "DF", "MF", "FW"]:
            pos_mask = self.df["Pos"] == position
            for feature in self.position_weights[position].keys():
                if feature.endswith("_z"):
                    raw_col = feature.replace("_z", "")  # Exempel: "Save%_z" → "Save%"
                    if raw_col in self.df.columns:  # Skyddar mot felaktiga kolumnnamn
                        self.df.loc[pos_mask, feature] = (
                        (self.df.loc[pos_mask, raw_col] - self.df.loc[pos_mask, raw_col].mean())
                    ) / self.df.loc[pos_mask, raw_col].std()

        for col in [col for col in self.df.columns if col.endswith("_z")]:
            self.df[col] = np.clip(self.df[col], -3, 3)


    def calculate_player_ratings(self):
        """
        Calculating position specific ratings for players
        """
        for position in ["GK", "DF", "MF", "FW"]:
            pos_mask = self.df["Pos"] == position
            for feature in self.position_weights[position].keys():
                if feature.endswith("_z") and feature in self.df.columns:
                    col = feature.replace("_z", "")
                    self.df.loc[pos_mask, feature] = (self.df.loc[pos_mask, col] - self.df.loc[pos_mask, col].mean()) / self.df.loc[pos_mask, col].std()

        self.df["PositionWeightedRating"] = self.df.apply(
            lambda row: self.calculate_single_rating(row),
            axis=1
        )
        self.df["LeagueMultiplier"] = self.df["League"].map(self.league_ratings).fillna(1.0)    
        self.df["PositionWeightedRating"] *= self.df["LeagueMultiplier"]
        self.scale_ratings("PositionWeightedRating")
        self.df["PositionWeightedRating"] = self.df["PositionWeightedRating_1_10"]
        
    def calculate_single_rating(self, row):
        position = row["Pos"]
        weights = self.position_weights.get(position, {})

        if not weights:
            return np.nan
        
        rating = 0.0
        sum_weights = 0.0

        for feature, weight in weights.items():
            if pd.notna(row[feature]):
                rating += weight * row[feature]
                sum_weights += weight  # Här samlar vi den FAKTISKA viktsumman

        # TA BORT DENNA RAD: sum_weights = sum(...) 

        if sum_weights > 0:
            rating /= sum_weights
        else:
            rating = np.nan
                
        return rating

    def get_top_players(self, n=10):
        """
        Hämtar de bästa spelarna baserat på deras position-specifika ratings.
        """
        top_players = self.df.nlargest(n, "PositionWeightedRating")
        return top_players[["Player", "Pos", "PositionWeightedRating"]]


    def validate_columns(self, required_columns):
        """
        Controlling that necessary columns exist
        """
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
    
    def scale_ratings(self, column):
        """
        Scaling ratings from 1-10 based on percentiles
        """
        for position in ["GK", "DF", "MF", "FW"]:
            pos_mask = self.df["Pos"] == position
            min_val = self.df.loc[pos_mask, column].min()
            max_val = self.df.loc[pos_mask, column].max()
            self.df.loc[pos_mask, f"{column}_1_10"] = 0.987 + 9 * ((self.df.loc[pos_mask, column] - min_val) / (max_val - min_val))

    def save_to_csv(self, filename):
        """
        Spara dataframen med spelarratings till en CSV-fil.
        """
        self.df.to_csv(filename, index=False)

if __name__ == "__main__":
    player_rating = PlayerRating(
        "../extracted_data/Cleaned_Standard_stats.csv", 
        "../extracted_data/Cleaned_Passing.csv",
        "../extracted_data/Cleaned_Goal_and_shot.csv",
        "../extracted_data/Cleaned_Defensive.csv",
        "../extracted_data/Cleaned_Goalkeeping.csv",
        "../extracted_data/Cleaned_Shooting.csv"
    )

    player_rating.load_and_merge_data()
    player_rating.clean_and_standardize()
    player_rating.calculate_player_ratings()

    player_rating.save_to_csv("Players.csv")
    top_players = player_rating.df.nlargest(20, "PositionWeightedRating")
    print(top_players[["Player", "Pos", "PositionWeightedRating", "Season"]])

