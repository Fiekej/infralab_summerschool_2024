import pandas as pd

years = [2021, 2022, 2023]
for year in years:
    print("starting", year)
    name = f"./datasets/{year}_FTS_dataset_en"
    df = pd.read_csv(f"{name}.csv", encoding="ISO-8859-1")

    horizon = df.loc[df["Programme name"] == "1.0.11 - Horizon Europe"]
    horizon.to_csv(f"{name}_HORIZON.csv")
