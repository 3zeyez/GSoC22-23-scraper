import csv
import progressbar
from src import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def filter():
    bar = progressbar.ProgressBar(maxval=172, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    CHROME_PATH = '/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    with open("csv_files/organizations.csv", "r") as f:
        organizations = csv.reader(f)
        filtred_organizations = []
        for organization in organizations:
            if organization[3] == 'Url':
                continue

            bar.update(int(organization[0]))

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                executable_path=CHROMEDRIVER_PATH, 
                options=chrome_options
            )

            url = organization[3]
            driver.get(url)
            driver.implicitly_wait(60)

            score = 0

            technologies_of_org = driver.find_element(By.CLASS_NAME, 'tech__content').text.split(", ")
            topics_of_org = driver.find_element(By.CLASS_NAME, 'topics__content').text.split(", ")

            matches_technologies = []
            for technology in my_technologies:
                if technology in technologies_of_org:
                    matches_technologies.append(technology)
            
            score_tech_according_me = len(matches_technologies * 100) / len(my_technologies)
            score_tech_according_org = len(matches_technologies * 100) / len(technologies_of_org)
            organization.append(", ".join(matches_technologies))
            
            matches_topics = []
            for topic in my_topics:
                if topic in topics_of_org:
                    matches_topics.append(topic)

            score_topic_according_me = len(matches_technologies * 100) / len(my_topics)
            score_topic_according_org = len(matches_topics * 100) / len(topics_of_org)
            organization.append(", ".join(matches_topics))

            score_according_me = (score_tech_according_me + score_topic_according_me) / 2
            score_according_org = (score_tech_according_org + score_topic_according_org) / 2
            organization.append(score_according_me)
            organization.append(score_according_org)
            
            if (matches_technologies != [] and matches_topics != []):
                try:
                    link = driver.find_element(By.XPATH, "/html/body/app-root/app-layout/mat-sidenav-container/mat-sidenav-content/div/div/main/app-program-organization/app-org-info/section/div[2]/div/div/div[1]/div/app-org-info-details/div/div[2]/a").text
                    organization.append(link)
                except:
                    link = None
                    pass
                try:
                    guidance_link = driver.find_element(By.XPATH, '/html/body/app-root/app-layout/mat-sidenav-container/mat-sidenav-content/div/div/main/app-program-organization/section/div/div[2]/a').text
                    organization.append(guidance_link)
                except:
                    guidance_link = None
                    pass

                filtred_organizations.append(organization)

                def sort_with_number(data):
                    return type(data[6]) == float and type(data[7]) == float

                filtred_organizations.sort(key=sort_with_number)

            driver.quit()

    bar.finish()


    with open("csv_files/filtred_organizations.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for organization in filtred_organizations:
            writer.writerow(organization)

if __name__ == "__main__":
    filter()
