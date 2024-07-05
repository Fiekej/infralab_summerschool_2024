import json
import pandas as pd
import re
import pycountry_convert as pc


# MERGE SUBSIDIARIES
def merge_organizations(organization_df):
    with open("head_orgs.txt", "r") as f:
        head_orgs = [o.lower() for o in f.read().split("\n")]
        head_orgs = [o for o in head_orgs if o.strip() != "" ]
    merged = {}

    for ho in head_orgs:
        merged[ho] = set()

    for i, r in organization_df.iterrows():
        for ho in head_orgs:
            found = True
            ho_i = 0
            for part in re.split('\s|-', ho.lower()):
                idxs = []
                if part not in re.split('\s|-', r["name"].lower()):
                    found = False
                    break
                else:
                    idxs.append(i)

                ho_i += 1

            if found is False: continue

            if not all((idxs[i] - idxs[i - 1] == 1) for i in range(1, len(idxs))):
                continue

            if found is True:
                print(r["name"], "->", ho)
                merged[ho].add(r["name"])
                organization_df.at[i, "name"] = ho
                break

    for o in merged:
        merged[o] = list(merged[o])

    with open("merged_orgs.json", "w+") as f:
        f.write(json.dumps(merged))


# COSTS
def fix_costs(organization_df):
    organization_df["totalCost"] = organization_df["totalCost"].apply(lambda x: float(str(x).replace(",", ".")))
    organization_df["netEcContribution"] = organization_df["netEcContribution"].apply(lambda x: float(str(x).replace(",", ".")))
    organization_df["ecContribution"] = organization_df["ecContribution"].apply(lambda x: float(str(x).replace(",", ".")))
    organization_df["diffContribution"] = organization_df["totalCost"] - organization_df["netEcContribution"]
    organization_df["diffContribution"] = organization_df["diffContribution"].apply(lambda x: x if x >= 0 else None)


# CONTINENT
def get_continent(country_code):
    if country_code == "EL" or country_code == "UK": return "EU"

    try:
        return pc.country_alpha2_to_continent_code(country_code)
    except Exception as e:
        print("country code erro:", e)
        return None


organization_df = pd.read_csv("./datasets/organization_cluster4.csv", encoding="ISO-8859-1")
merge_organizations(organization_df)
fix_costs(organization_df)
organization_df["continent"] = organization_df["country"].apply(lambda x: get_continent(x))


organization_df.to_csv("./datasets/organizations_cluster4_headorgs.csv")
