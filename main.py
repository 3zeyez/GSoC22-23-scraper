from scrape_organizations import scrape
from filter_organizations import filter
from getTop10 import get_top10


def get_url():
    return input("Enter the GSoC website url: ")
    

def main():
    url = get_url()

    if url != "":
        scrape(url)
    else:
        print("You're using the default web site url!")
        print("Url: https://summerofcode.withgoogle.com/programs/2023/organizations")
        scrape()  

    filter()
    get_top10()


if __name__ == "__main__":
    main()
