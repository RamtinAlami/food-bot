import csv
import requests
from bs4 import BeautifulSoup
import time
import json
from parser import AR_parser

# NEED TO IMPLEMENT A START AND END SO SMALLER SECTIONS CAN BE PARSED
class Bot:
    def __init__(self, sitemap, pause_time):
        self.pause_time = pause_time
        self.urls = self.get_links(self.get_soup(sitemap))
    
    def get_soup(self, sitemap):
        with open(sitemap) as file:
            source = file.read()
        soup = BeautifulSoup(source, 'lxml')
        return soup
    
    def get_links(self, soup):
        url_list_tags = soup.findAll("loc")
        url_list = [url_list_tag.text for url_list_tag in url_list_tags]
        return url_list

class KG_agent(Bot):
    def __init__(self, sitemap):
        pass

class AR_agent(Bot):
    def parse(self, url):
        parser = AR_parser(url)
    
    def post(self):
        pass

if __name__ == "__main__":
    html_source = "recipedetail.xml"
    parser = AR_agent(html_source, 1.0)
    print(len(parser.urls))
