from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import csv
import os
from write_csv import *

class Browser:
    def __init__(self, browser):
        self.browser=browser
   
    def get_html(self,url):
        self.browser.get(url)
        return self.browser.page_source