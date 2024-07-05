import pandas as pd

VATs_FTS = set()
years = [2021, 2022, 2023]
for year in years:
    print("starting", year)
    df = pd.read_csv(f"./datasets/{year}_FTS_dataset_en_HORIZON.csv", encoding="ISO-8859-1")
    VATs_FTS_df = df["VAT number of beneficiary"]
    for vat in VATs_FTS_df:
        VATs_FTS.add(vat)

VATs_organization = set()
df = pd.read_csv("../datasets/organization.csv")
VATs_org_df = df["vatNumber"]
for vat in VATs_org_df:
    VATs_organization.add(str(vat))

VATS_diff = VATs_FTS.difference(VATs_organization)

with open("unq_vats.txt", "w+") as f:
    f.write("\n".join(VATS_diff))

print("total:", len(VATs_FTS) + len(VATs_organization))
print("difference:", len(VATS_diff))
