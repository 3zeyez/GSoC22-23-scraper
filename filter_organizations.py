import csv
from keywords import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

with open("organizations.csv", "r") as f:
    organizations = csv.reader(f)
    filtred_organizations = []
    for organization in organizations:
        if organization[3] == 'Url':
            continue

        url = organization[3]
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(30)

        technologies_of_org = driver.find_element(By.CLASS_NAME, 'tech__content').text
        topics_of_org = driver.find_element(By.CLASS_NAME, 'topics__content').text

        nb_technologies = len([technology for technology in technologies if technology in technologies_of_org])
        organization.append(nb_technologies)
        
        nb_topics = len([topic for topic in topics if topic in topics_of_org])
        organization.append(nb_topics)
        
        if (nb_technologies != 0 or nb_topics != 0):
            try:
                div_of_link_of_org = driver.find_element(By.CSS_SELECTOR, 'div.link-wrapper')
                link = driver.find_element(By.XPATH, './/a').get_attribute('href')
                organization.append(link)
            except:
                link = None
                pass
            try:
                div_of_guidance_link = driver.find_element(By.CSS_SELECTOR, 'div.link-wrapper.ng-star-inserted')
                guidance_link = driver.find_element(By.XPATH, './/a').get_attribute('href')
                organization.append(guidance_link)
            except:
                guidance_link = None
                pass

            filtred_organizations.append(organization)
        driver.quit()

with open("filtred_organizations.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["ONo", "Name", "Desc", "Url", "Nb Tech", "Nb Topics", "Org link", "Guidance link"])

    i = 0
    for organization in filtred_organizations:
        i += 1
        writer.writerow(organization)
