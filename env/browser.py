from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import csv
import os
from write_csv import *
browser = webdriver.Chrome(executable_path="E:\driver\chromedriver.exe")


def get_html(url):
    browser.get(url)
    return browser.page_source