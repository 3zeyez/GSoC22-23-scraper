import csv
import pandas as pd 

def get_top10():
    data = pd.read_csv("csv_files/filtred_organizations.csv")
    data.sort_values(by="Score", ascending=False, inplace=True)
    organizations = data.values.tolist()

    top10 = []
    for i in range(10):
        top10.append(organizations[i])

    with open("csv_files/Top10.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(top10)

if __name__ == "__main__":
    get_top10()