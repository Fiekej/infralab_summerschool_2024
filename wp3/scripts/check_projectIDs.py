import pandas as pd

tech_df = pd.read_csv("./datasets/tech_projects_categorized_v2.csv")
org_df = pd.read_csv("./datasets/organizations_cluster4_headorgs.csv")

ids_tech = set(tech_df["projectID"])
ids_org = set(org_df["projectID"])

only_tech = ids_tech - ids_org
only_org = ids_org - ids_tech
print(only_tech)


print("only tech", len(only_tech))
for val in only_tech:
    print(val, val in org_df["projectID"].values)
print()
print("only org", len(only_org))
for val in only_tech:
    print(val, val in tech_df["projectID"].values)
