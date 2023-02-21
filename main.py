from keywords import technologies, topics
from bs4 import BeautifulSoup
import requests as req

url = "https://summerofcode.withgoogle.com/programs/2022/organizations"
page = req.get(url)

soup = BeautifulSoup(page.content, "lxml")
organizations = soup.find_all("div", {"class": "org-wrapper"})
print(organizations)
