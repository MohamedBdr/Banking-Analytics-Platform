import os
from kaggle.api.kaggle_api_extended import KaggleApi

DATASET = "ealtman2019/credit-card-transactions"
RAW_PATH = "data/raw"

def download_dataset():
    os.makedirs(RAW_PATH, exist_ok=True)

    print("🚀 Downloading dataset from Kaggle...")

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files(
        DATASET,
        path=RAW_PATH,
        unzip=True
    )

    print("✅ Dataset downloaded successfully into data/raw")

if __name__ == "__main__":
    download_dataset()
    