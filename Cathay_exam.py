from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import numpy as np

conn = MongoClient()
db = conn.rent591
collection = db.rent591Taipei

def clean_identity(identity):
    if "屋主" in identity:
        return "屋主"
    elif "仲介" in identity:
        return "仲介"
    elif "代理人" in identity:
        return "代理人"
    else:
        return identity

def crawl_and_insert(url,region):
    try:
        browser.get("https://"+url)
        person = browser.find_element_by_xpath("//*[@id=\"main\"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/i").text
        identity = browser.find_element_by_xpath("//*[@id=\"main\"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]").text
        identity = clean_identity(identity)
        phone = browser.find_element_by_xpath("//*[@id=\"main\"]/div[3]/div[2]/div[2]/div[2]/div[2]/span[2]").get_attribute('data-value')
        explain1 = browser.find_element_by_xpath("//*[@id=\"main\"]/div[3]/div[2]/div[2]/div[1]/ul").text
        if "型態" in explain1:
            building_type = explain1.split("型態 :")[1].lstrip().split("\n")[0]
        else:
            building_type = None
        if "現況" in explain1:
            current_condition = explain1.split("現況 :")[1].lstrip().split("\n")[0]
        else:
            current_condition = None

        explain2 = browser.find_element_by_xpath("//*[@id=\"main\"]/div[3]/div[2]/div[1]/ul[1]").text
        if "性別要求" in explain2:
            gender = explain2.split("性別要求\n：")[1].lstrip().split("\n")[0]
        else:
            gender = None
        collection.insert_one({"url": url, "地區": region, "出租者": person, "出租者身份": identity, "聯絡電話": phone, "型態": building_type, "現況": current_condition, "性別要求": gender})
    except:
        pass

links = []
url = "https://rent.591.com.tw/?kind=0&region=1&shType=list"
driverLocation = "/Users/estrella/Downloads/download/chromedriver"
browser = webdriver.Chrome(driverLocation)
browser.get(url)
browser.find_element_by_xpath("//*[@id=\"area-box-close\"]").click()
# while True:
for j in np.arange(4):
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    h3 = soup.select("h3")
    links += [str(i).split("//")[1].split("html")[0]+"html" for i in h3]
    try:
        next_page = browser.find_element_by_class_name("pageNext")
        browser.execute_script("arguments[0].click();", next_page)
    except:
        break
for link in links:
    crawl_and_insert(link,"台北市")

nt_links = []
url = "https://rent.591.com.tw/?kind=0&region=3&shType=list"
driverLocation = "/Users/estrella/Downloads/download/chromedriver"
browser = webdriver.Chrome(driverLocation)
browser.get(url)
browser.find_element_by_xpath("//*[@id=\"area-box-body\"]/dl[1]/dd[2]").click()
# while True:
for j in np.arange(4):
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    h3 = soup.select("h3")
    nt_links += [str(i).split("//")[1].split("html")[0]+"html" for i in h3]
    try:
        next_page = browser.find_element_by_class_name("pageNext")
        browser.execute_script("arguments[0].click();", next_page)
    except:
        break
for link in nt_links:
    crawl_and_insert(link,"新北市")