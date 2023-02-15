from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import json

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  ##we using Service object


def shortest_path(txid):
    driver.get("https://www.blockchain.com/explorer/transactions/btc/" + txid)
    # assert "Python" in driver.title
    # elem = driver.find_element(By.XPATH, "//span[text()='Coinbase']")
    time.sleep(3)  # there is handler for that
    #clicking json button
    search = driver.find_element(By.XPATH,
                                 "/html/body/div/div[2]/div[2]/main/div/div/section/section/div[3]/div[1]/button[2]")
    search.click()
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    # getting my json file
    search = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    "/html/body/div/div[2]/div[2]/main/div/div/section/section/div[3]/div[2]/div/div/div/pre")))

    search_str = search.text
    #print(search_str)
    graph = json.loads(search_str)
    print("iam at other web", graph["txid"])
    queue = []
    if graph["inputs"][0]["coinbase"] and graph["block"]["height"] == 730390:
        print("I found coinbase")
    elif graph["inputs"][0]["coinbase"] == True:
        return

    else:  ##i need to do for loop here and call recursion
        # i need to go over inputsts
        #shortest_path(graph["txid"])
        for item in graph["inputs"]:
            #now i want to insert to search bar
            search_box = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/div/div[2]/div/div[2]/form/input")))
            # search_box.send_keys(" ")
            search_box.send_keys(item["txid"])
            print(item["txid"])
            search_box.send_keys(Keys.RETURN)  # pressing enter //here i will clear the page


            wait = WebDriverWait(driver, 10) #finding to click second page
            found_box = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/main/div/div/div[1]/div/div/a/div/div/div[2]")))
            #found_box = driver.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/main/div/div/div[1]/div/div/a/div/div/div[2]")
            found_box.click() #clicking  icon to move to the page
            #search_box.send_keys().clear()
            shortest_path(item["txid"])

shortest_path("79ec6ef52c0a2468787a5f671f666cf122f68aaed11a28b15b5da55c851aee75")
