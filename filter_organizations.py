import csv
from keywords import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def filter():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    with open("csv_files/organizations.csv", "r") as f:
        organizations = csv.reader(f)
        filtred_organizations = []
        for organization in organizations:
            if organization[3] == 'Url':
                continue

            url = organization[3]
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
            driver.implicitly_wait(60)

            score = 0

            technologies_of_org = driver.find_element(By.CLASS_NAME, 'tech__content').text.split(", ")
            topics_of_org = driver.find_element(By.CLASS_NAME, 'topics__content').text.split(", ")

            matches_technologies = []
            for technology in technologies_of_org:
                if technology in my_technologies:
                    matches_technologies.append(technology)
                    score += 10 
                else: 
                    score -= 5

            organization.append(", ".join(matches_technologies))
            
            matches_topics = []
            for topic in topics_of_org:
                if topic in my_topics:
                    matches_topics.append(topic)
                    score += 10 
                else: 
                    score -= 5

            organization.append(", ".join(matches_topics))

            organization.append(score)
            
            if (matches_technologies != [] and matches_topics != []):
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

                def sort_with_number(data):
                    return type(data[6]) == int

                filtred_organizations.sort(key=sort_with_number)

            driver.quit()

    with open("csv_files/filtred_organizations.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Org No", "Name", "Desc", "Url", "Technologies", "Topics", "Score", "Org link", "Guidance link"])

        for organization in filtred_organizations:
            writer.writerow(organization)

if __name__ == "__main__":
    filter()
