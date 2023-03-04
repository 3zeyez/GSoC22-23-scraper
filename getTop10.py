import csv
import pandas as pd
from src import header


def get_top10():
    # load the data and sort it to get the top 10 orgs according to my score
    data = pd.read_csv("csv_files/filtred_organizations.csv")
    data.sort_values(by="My Score", ascending=False, inplace=True)
    organizations = data.values.tolist()

    mytop10 = [header]
    for i in range(10):
        mytop10.append(organizations[i])

    with open("csv_files/MyTop10.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(mytop10)

    # reload the data and sort it to get the top 10 orgs according to org score
    data = pd.read_csv("csv_files/filtred_organizations.csv")
    data.sort_values(by="Org Score", ascending=False, inplace=True)
    organizations = data.values.tolist()

    orgtop10 = [header]
    for i in range(10):
        orgtop10.append(organizations[i])

    with open("csv_files/OrgTop10.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(orgtop10)

    # relaod the data and sort it to get the top 10 orgs according to the avg score
    data = pd.read_csv("csv_files/filtred_organizations.csv")
    data.sort_values(by="Score", ascending=False, inplace=True)
    organizations = data.values.tolist()

    top10 = [header]
    for i in range(10):
        top10.append(organizations[i])

    with open("csv_files/Top10.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(top10)


if __name__ == "__main__":
    get_top10()
