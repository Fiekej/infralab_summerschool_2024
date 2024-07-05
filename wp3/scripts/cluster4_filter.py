import pandas as pd

project_df = pd.read_csv("../datasets/project.csv")
organization_df = pd.read_csv("../datasets/organization.csv", encoding="ISO-8859-1")

project_df['topic_part'] = project_df['topics'].str.split('-').str[1]
cluster4_ids = project_df.loc[project_df['topic_part'] == 'CL4']

project_ids = cluster4_ids.iloc[:, 0]

cluster4 = organization_df.loc[organization_df["projectID"].isin(project_ids)]

cluster4.to_csv("./datasets/organization_cluster4.csv")
