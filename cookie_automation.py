from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import datetime


def check_for_accessory():

    global accessory_dict
    money = driver.find_element(By.ID, "money")
    formatted_money = int(money.text.replace(",", ""))

    for price_value, accessory_id_value in sorted(accessory_dict.items(), reverse=True):

        if formatted_money >= price_value:
            print(price_value, accessory_id_value)
            driver.find_element(By.ID, accessory_id_value).click()
            break


def timer():

    return datetime.datetime.now() + datetime.timedelta(seconds=5)


service_obj = Service("/Users/brandonho/Development/chromedriver")
driver = webdriver.Chrome(service=service_obj)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# get id list for each cookie accessory
accessory_ids = driver.find_elements(By.CSS_SELECTOR, "#store div")
# remove last id value---not applicable
accessory_ids.pop()

# get price list for each cookie accessory
accessory_price = driver.find_elements(By.CSS_SELECTOR, "#store div b")

#  format accessory price list
accessory_price_list = []
for item in accessory_price:
    price = item.text
    if price != "":
        index = price.index("-")
        accessory_price_list.append(int(price[index + 2:].replace(",", "")))

# create dictionary combining price and associated id
accessory_dict = {}
for index, accessory_id in enumerate(accessory_ids):
    accessory_dict[accessory_price_list[index]] = accessory_id.get_attribute("id")

# start program timer 5 mins
endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)

# start 5 second timer
check_time = timer()

while True:

    if datetime.datetime.now() >= endTime:
        break

    if datetime.datetime.now() >= check_time:
        check_for_accessory()
        check_time = timer()
    else:
        driver.find_element(By.ID, "cookie").click()

cookie_rate = driver.find_element(By.ID, "cps")
print(f"{cookie_rate.text}")
driver.quit()
