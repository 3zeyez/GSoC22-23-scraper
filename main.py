from scrape_organizations import scrape
from filter_organizations import filter
from getTop10 import get_top10


def main():
    scrape()
    filter()
    get_top10()


if __name__ == "__main__":
    main()
