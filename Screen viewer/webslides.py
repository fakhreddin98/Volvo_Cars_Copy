# pip install selenium måste installeras
# https://msedgedriver.azureedge.net/111.0.1661.51/edgedriver_win64.zip

import tkinter
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# set the path to your Microsoft Edge webdriver executable
edge_path = r"C:\Users\fkabawe\Documents\msedgedriver.exe"

# create a new Microsoft Edge webdriver instance
driver = webdriver.Edge(executable_path=edge_path)

urls = [
    "https://app.powerbi.com/groups/me/apps/c7ad8b88-4322-4f17-a072-ca26bd3e7e92/reports/02d85ff0-bcc3-49df-a65e-40850b8b1fc8/ReportSection3e46342d2f1ccbe3342a?ctid=81fa766e-a349-4867-8bf4-ab35e250a08f",
    "https://app.powerbi.com/groups/me/apps/c7ad8b88-4322-4f17-a072-ca26bd3e7e92/reports/02d85ff0-bcc3-49df-a65e-40850b8b1fc8/ReportSectiona8d51c35a997c2053410?ctid=81fa766e-a349-4867-8bf4-ab35e250a08f",
    "https://jira-vira.volvocars.biz/plugins/servlet/Wallboard/?dashboardId=35449&dashboardId=31051&cyclePeriod=30000&transitionFx=none&random=false"
]


driver.get(urls[0])

for url in urls[1:]:
    driver.execute_script(f"window.open('{url}')")

# get the handles of all the open tabs
tab_handles = driver.window_handles

# switch to the first tab
current_tab = 0

# iterate through the URLs
while True:
    # navigate to the URL
    current_tab = (current_tab + 1) % len(tab_handles)
    driver.switch_to.window(tab_handles[current_tab])

    # wait for the "Refresh" button to become clickable
    try:
        refresh_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reportAppBarRefreshBtn")))
        ActionChains(driver).move_to_element(refresh_button).click(refresh_button).perform()
        print ("refreash excuted")  
        time.sleep(10)

    except:
        # if the URL is not a Power BI website, wait for 60 seconds before moving to the next URL
        time.sleep(10)
        continue
