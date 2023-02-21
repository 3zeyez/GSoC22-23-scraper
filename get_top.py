import csv


with open("filtred_organizations.csv", "r") as f:
    organizations = csv.reader(f)

    top_organizations = []
    for organization in organizations:
        if organization[1] == "Name":
            continue

        if organization[4] != '0' and organization[5] != '0':
            top_organizations.append(organization)

with open("Top_organizations.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["ONo", "Name", "Desc", "Url", "Nb Tech", "Nb Topics", "Org link", "Guidance link"])

    i = 0
    for organization in top_organizations:
        i += 1
        print(organization[1], organization[4], organization[5])
        writer.writerow(organization)
