import csv
# import requests
from bs4 import BeautifulSoup
import time
import json
from parser import AR_parser, GK_parser

# NEED TO IMPLEMENT A START AND END SO SMALLER SECTIONS CAN BE PARSED
class Bot:
    BOT_ID_COUNTER = 0
    def __init__(self, sitemaps, pause_time, parser):
        self.pause_time = pause_time
        self.sitemaps = sitemaps
        self.current_sitemap_urls = self.get_current_sitemap().urls
    
    def get_current_sitemap(self):
        pass

    def get_soup(self, sitemap):
        with open(sitemap) as file:
            source = file.read()
        soup = BeautifulSoup(source, 'lxml')
        return soup
    
    def get_links(self, soup):
        url_list_tags = soup.findAll("loc")
        url_list = [url_list_tag.text for url_list_tag in url_list_tags]
        return url_list
    
    def add_sitemap(self, soup):
        pass
    
    def force_pause(self):
        pass

class MasterBot:
    def __init__(self, bots):
        self.bots = []
        self.schedule = Schedule(self.bots)
    
    def add_bot(self, sitemaps, pause_time, parser):
        pass
    
    def run(self):
        pass
    

# TODO REQUIRES A LOT OF TESTING
class Schedule:
    def __init__(self, bots):
        self.bots = bots
        self.schedule = self.find_schedule()
    
    def __next__(self):
        # returns a tuple (bot, pause_time) everytime called
        index = 0
        while True:
            output = self.schedule[index % len(self.schedule)]
            index += 1 
            yield output
    
    # TODO add a scheduling functions here
    def find_schedule(self):
        pass
    
    def add_bot(self, bot, pause_time):
        self.bots.append((bot, pause_time))
    
    def remove_bot(self, bot):
        for bot_object, pause_time in self.bots:
            if bot_object == bot:
                self.bots.remove((bot_object, pause_time))
                break
        self.schedule = self.find_schedule()
        
    
    

class Sitemap:
    def __init__(self, xml_file):
        self.urls = self.extract_links(self.get_xml_soup(xml_file))
    
    def get_xml_soup(self, xml_file):
        with open(xml_file) as file:
            source = file.read()
        soup = BeautifulSoup(source, 'lxml')
        return soup
    
    def extract_links(self, soup):
        link_tags = soup.findAll('loc')
        links = [link_tag.text for link_tag in link_tags]
        return links
    
    def __next__(self):
        for url in self.urls:
            yield url

    def __iter__(self):
        return self

if __name__ == "__main__":
    html_source = "recipedetail.xml"
    sitemap = Sitemap(html_source)
    print(sitemap.urls)
