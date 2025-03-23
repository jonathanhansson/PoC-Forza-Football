import zipfile
import pandas as pd
import os

#======================================================
# The "DataLoader"-class has a function which runs the pipeline, which is "process_data"
# The "DataLoader"-class also has a function which extracts zip-files from the dataset
# The "DataLoader"-class, when instan (__init__), also creates a new folder which then contains the extracted data in csv-files which are readable for Pandas 
#======================================================

class DataLoader:
    def __init__(self, zip_folder: str, extract_folder: str = "extracted_data"):
        self.zip_folder = zip_folder
        self.extract_folder = extract_folder
        os.makedirs(self.extract_folder, exist_ok=True)

    def extract_zip_files(self):
        for file in os.listdir(self.zip_folder):
            if file.endswith(".zip"):
                zip_path = os.path.join(self.zip_folder, file)
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(self.extract_folder)
                print(f"Extraherade: {file}")

    def load_csv_files(self) -> dict:
        dataframes = {}

        for file in os.listdir(self.extract_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(self.extract_folder, file)
                df = pd.read_csv(file_path)
                dataframes[file] = df
                print(f"Laddade in: {file} ({df.shape[0]} rader, {df.shape[1]} kolumner)")
        return dataframes
    
    def process_data(self):
        self.extract_zip_files()
        return self.load_csv_files()
