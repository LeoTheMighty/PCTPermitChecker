import sys
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time

BASE_URL = "https://permit.pcta.org/application/"
WEBHOOK_URL = "https://maker.ifttt.com/trigger/pcta_availability/with/key/cFZBPNUAflwgR0tTUirdXh"

def main_bs():
    base_page = requests.get(BASE_URL)
    soup = BeautifulSoup(base_page.content, 'html.parser')
    print(base_page.content)

def get_avail(elements):
    cap = []
    for e in elements:
        cap.append(e.text)
    return cap

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE_URL)
    driver.find_element_by_class_name("continue.button").click()
    driver.implicitly_wait(15)
    Select(driver.find_element_by_id("start_location_id")).select_by_value("1")
    Select(driver.find_element_by_id("end_location_id")).select_by_value("116")
    driver.find_element_by_class_name("continue.button").click()
    start_date = {
        "march": 20,
        "april": 1,
        "may": 1
    }
    month_days = {
        "march": [],
        "april": [],
        "may": []
    }
    month_days["march"] = get_avail(driver.find_elements_by_class_name("fc-day-grid-event"))
    driver.find_element_by_class_name("fc-next-button").click()
    month_days["april"] = get_avail(driver.find_elements_by_class_name("fc-day-grid-event"))
    driver.find_element_by_class_name("fc-next-button").click()
    month_days["may"] = get_avail(driver.find_elements_by_class_name("fc-day-grid-event"))
    num_days = len(month_days["march"]) + len(month_days["april"]) + len(month_days["may"])
    print("Checking " + str(num_days) + " days:")
    if num_days != 73:
        print("WHY DID THIS FAIL?? WEBSITE GOT WRONG DATA?")
        requests.get("https://maker.ifttt.com/trigger/pcta_availability/with/key/cFZBPNUAflwgR0tTUirdXh", data={ "value1": "ERROR: ", "value2": "GOT A BAD AMOUNT OF days check just in case?" })
        driver.close()
        return False
    for month, days in month_days.items():
        for i, t in enumerate(days):
            d = start_date[month] + i
            if t == "50":
                # print("{} {}. nope".format(month, d))
                pass
            else:
                print("{} {}. OMG LET'S GO".format(month, d))
                pcta_availability
                requests.get(WEBHOOK_URL, data={ "value1": month, "value2": d })
                driver.close()
                return True
    driver.close()
    return False

if __name__ == "__main__":
    if main():
        sys.exit(1)
    sys.exit(0)
    # main_bs()
