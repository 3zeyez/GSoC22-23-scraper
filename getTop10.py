import csv
import pandas as pd 
from src import header


def get_top10():
    data = pd.read_csv("csv_files/filtred_organizations.csv")
    data.sort_values(by="My Score", ascending=False, inplace=True)
    organizations = data.values.tolist()

    mytop10 = [header]
    for i in range(10):
        mytop10.append(organizations[i])

    with open("csv_files/MyTop10.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(mytop10)

    data = pd.read_csv("csv_files/filtred_organizations.csv")
    data.sort_values(by="Org Score", ascending=False, inplace=True)
    organizations = data.values.tolist()

    orgtop10 = [header]
    for i in range(10):
        orgtop10.append(organizations[i])

        with open("csv_files/OrgTop10.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(orgtop10)

if __name__ == "__main__":
    get_top10()
