import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = 'https://summerofcode.withgoogle.com/programs/2022/organizations'
driver.get(url)
driver.implicitly_wait(30) # wait the web site to load

# to get 100 organization instead of 50
button = driver.find_element(By.CLASS_NAME, 'ng-tns-c141-5')
button.send_keys(Keys.DOWN)


def save_organizations(nb=0):
    organizations = driver.find_elements(By.CSS_SELECTOR, 'div.card')
    i = nb
    for organization in organizations:
        i += 1
        driver.implicitly_wait(3)
        name = organization.find_element(By.CLASS_NAME, 'name').text
        desc = organization.find_element(By.CLASS_NAME, 'short-description').text
        link = organization.find_element(By.XPATH, './/a')
        url = link.get_attribute('href')
        writer.writerow([i, name, desc, url])
    return i


with open("organizations.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["ONo", "Name", "Desc", "Url"])

    nb = save_organizations()

    next_page = driver.find_element(By.XPATH, '/html/body/app-root/app-layout/mat-sidenav-container/mat-sidenav-content[1]/div/div/main/app-program-organizations/app-orgs-grid/section[2]/div/mat-paginator/div/div/div[2]/button[2]')
    next_page.send_keys(Keys.ENTER)

    save_organizations(nb)
