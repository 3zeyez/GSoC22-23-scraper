import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def scrape(url="https://summerofcode.withgoogle.com/programs/2023/organizations"):
    # make chrome window doesn't close automaticly 
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # setup driver for chrome browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                            options=chrome_options)

    # connect to the website
    driver.get(url)
    driver.implicitly_wait(30)  # wait the web site to load

    # to get 100 organization loaded in single page instead of 50
    button = driver.find_element(By.CLASS_NAME, 'ng-tns-c141-5')
    button.send_keys(Keys.DOWN)
    driver.implicitly_wait(3)  # wiat til the page get reloaded

    number_of_orgs = driver.find_element(By.CLASS_NAME, 'mat-paginator-range-label').text
    print(number_of_orgs)
    number_of_orgs = 172  # int(number_of_orgs[-3:])


    def save_organizations(nb=0):  # nb is used to know the previous number of orgs
        # find all the organizations cards
        organizations = driver.find_elements(By.CSS_SELECTOR, 'div.card')

        # iterate through organizations and get info about each one of them
        for organization, org_num in zip(organizations, [i for i in range(nb, nb + len(organizations))]):
            name = organization.find_element(By.CLASS_NAME, 'name').text
            desc = organization.find_element(By.CLASS_NAME, 'short-description').text
            link = organization.find_element(By.XPATH, './/a')
            url = link.get_attribute('href')
            writer.writerow([org_num, name, desc, url])
        

    # save organizations' info in a csv file
    with open("csv_files/organizations.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Num", "Name", "Description", "Url"])

        
        for i in range(number_of_orgs // 100 + 1):
            save_organizations(i * 100)  # each itiration saves the loaded orgs

            # move to the next page, which contains the second 100 organization
            # if we are not in the last page
            if i != number_of_orgs // 100:
                next_page = driver.find_element(By.XPATH, '/html/body/app-root/app-layout/mat-sidenav-container/mat-sidenav-content[1]/div/div/main/app-program-organizations/app-orgs-grid/section[2]/div/mat-paginator/div/div/div[2]/button[2]')
                next_page.send_keys(Keys.ENTER)

    driver.quit()


if __name__ == "__main__":
    scrape()