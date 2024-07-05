import json
import pandas as pd

org_df = pd.read_csv("./datasets/organizations_cluster4_headorgs.csv", encoding="ISO-8859-1")
tech_df = pd.read_csv("./datasets/tech_projects_categorized_v2.csv")

merged_df = pd.merge(org_df, tech_df[['projectID', 'taxonomyObjective']], on='projectID', how='left')

with open("cluster_tech_keywords.json", "r") as f:
    bigger = json.loads(f.read())

org_tech = {}
for _, r in merged_df.iterrows():
    name = r["name"]
    if name not in org_tech:
        org_tech[name] = {}

    keywords = r["taxonomyObjective"].split(",")
    for k in keywords:
        if k in bigger:
            k = bigger[k]
        if k in org_tech[name]:
            org_tech[name][k] += r["netEcContribution"]
        else:
            org_tech[name][k] = r["netEcContribution"]

most_money = []
for org in org_tech:
    value, key = max([(value, key) for key, value in org_tech[org].items()])
    if value == 0:
        continue
    most_money.append((org, key, value))

big_df = pd.DataFrame(most_money, columns=["name", "biggest_key", "value"])
merged_df = pd.merge(merged_df, big_df[['name', 'biggest_key']], on='name', how='left')
merged_df.to_csv("./datasets/organizations_cluster4_tech.csv")
