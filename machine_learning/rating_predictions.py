import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

class PlayerPrediction:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def prepare_data(self):
        # Definiera features (X) och target (y)
        features = [
            "GoalsPer90", "YelloCards", "AssistPer90", "NonPenaltyGoalsPer90", "GoalsandAssistPer90", "ProgressiveCarries", "ProgressivePasses", "Cmp%", "PrgDist", "GCA90", "SCA90", "Total_Tackles", "Tackles_Won", "Interceptions", "Tackles_Def_3rd", "Tackles_mid_3rd", "Shots_Blocked", "Save%", "GA90", "CS%", "W", "GoalsPerShotOnTarget"
        ]
        
        X = self.df[features]  # Funktioner (X)
        y = self.df["PositionWeightedRating_1_10"]  # Target (y)

        combined = pd.concat([X, y], axis=1)
        combined = combined.dropna(subset=["PositionWeightedRating_1_10"])

        X_clean = combined[features]
        y_clean = combined["PositionWeightedRating_1_10"]

        # Dela upp i tränings- och testdata
        X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.15, random_state=42)

        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train):
        # Träna en Random Forest Regressor-modell
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model

    def evaluate_model(self, model, X_test, y_test):
        # Gör prediktioner
        y_pred = model.predict(X_test)

        # Beräkna MSE (Mean Squared Error) och R² (R-squared)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Mean Squared Error: {mse}")
        print(f"R²: {r2}")

        return y_pred

if __name__ == "__main__":
    # Här ser vi till att filvägen stämmer för CSV-filen med spelardata
    prediction = PlayerPrediction("Players.csv")

    # Förbered data
    X_train, X_test, y_train, y_test = prediction.prepare_data()

    # Träna modellen
    model = prediction.train_model(X_train, y_train)

    # Utvärdera modellen
    y_pred = prediction.evaluate_model(model, X_test, y_test)

    # Om du vill skriva ut de första prediktionerna
    print("Predictions on Test Data:")
    print(y_pred[:10])

    player_names = X_test.index

    predictions_with_index = pd.DataFrame({"Player": player_names, "Player rating": y_pred})
    print(predictions_with_index.head(30).sort_values(by="Player rating", ascending=False))