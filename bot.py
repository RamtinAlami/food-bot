import csv
# import requests
from bs4 import BeautifulSoup
import time
import json
from parser import AR_parser, GK_parser 
import logging
import pprint
from data_save import  csv_publisher

# NEED TO IMPLEMENT A START AND END SO SMALLER SECTIONS CAN BE PARSED
class Bot:
    BOT_ID_COUNTER = 0
    def __init__(self, sitemaps_files, pause_time, parser):
        self.pause_time = pause_time
        self.sitemaps_files = self.sitemaps(sitemaps_files)
        self.sitemap_url_generator = next(self.sitemaps_files)
        self.time_of_last_request = time.time()
        self.id = Bot.BOT_ID_COUNTER
        self.parser = parser
        Bot.BOT_ID_COUNTER += 1
        self.counter = 0

        field_names = ["id", "name", "url", "ingredients", "directions", "rating",
        "img_link", "categories", "time", "publisher", "meta", "food_yield",
        "description", "nutrition", "reviews"]
        self.csv_file = csv_publisher("genius-kitchen-recipes", field_names)
    
    def sitemaps(self, sitemaps_files):
        for sitemap_file in sitemaps_files:
            try:
                sitemap = Sitemap(sitemap_file)
                yield iter(sitemap)
            except:
                pass
        raise AssertionError("End of sitemaps")
        

    def parse(self, url):
        try:
            site = self.parser(url)
            data = site.get_data_dictionary()
            return data
        except ConnectionError:
            error = "ConnectionError at Bot.parse for " + url
            logging.warning(error)
            pass
        except TypeError:
            error = "TypeError at Bot.parse for " + url
            logging.warning(error)
        except Exception as e:
            error = str(e) + " at Bot.parse for " + url
            logging.error(error)

    
    def publish(self, data_dict):
        # TODO add try and exception for future scalability
        self.csv_file.write(data_dict)


    def get_url(self):
        while True:
            try:
                return next(self.sitemap_url_generator)
            except StopIteration:
                self.sitemap_url_generator = next(self.sitemaps_files)
                logging.warning("StopIteration at bot.get_url")
            except Exception as e:
                error = str(e) + " at Bot.get_url"
                logging.error(error)
            
    
    def force_pause(self, pause_time):
        while (time.time() - self.time_of_last_request) < pause_time:
            time.sleep(0.01)
    
    def run(self):
        self.force_pause(self.pause_time)
        url = self.get_url()
        print(url)
        data_dict = self.parse(url)
        self.add_id(data_dict)
        self.time_of_last_request = time.time()
        self.publish(data_dict)
    
    def add_id(self, data_dict):
        data_dict["id"] = self.id
        self.id += 1

class MasterBot:
    def __init__(self, bots):
        self.bots = bots
        self.update_schedule()
    
    def add_bot(self, sitemaps, pause_time, parser):
        new_bot = Bot(sitemaps, pause_time, parser)
        self.bots.append(new_bot)
        self.update_schedule()
    
    def update_schedule(self):
        self.schedule = Schedule(self.bots)
        self.schedule = iter(self.schedule)
    
    def remove_bot(self, bot):
        for bot_object, pause_time in self.bots:
            if bot_object == bot:
                self.bots.remove(bot)
                self.update_schedule()
                return
        else:
            raise ValueError

    def run(self):
        while True:
            bot, pause_time = next(self.schedule)
            bot.run()
            time.sleep(pause_time)
    
    def run_bot(self, bot):
        try:
            bot.run()
        except AssertionError:
            self.remove_bot(bot)
            self.run()
        except Exception as e:
            logging.error(e)
    

class Schedule:
    def __init__(self, bots):
        self.bots = bots
        self.schedule = self.find_schedule()
    
    def __iter__(self):
        # returns a tuple (bot, pause_time) everytime called
        index = 0
        while True:
            output = self.schedule[index % len(self.schedule)]
            index += 1 
            yield output
    
    # TODO add a proper scheduling functions here
    def find_schedule(self):
        output = []
        pause_time = 1/len(self.bots)
        for bot in self.bots:
            output.append((bot, pause_time))
        return output
    
    def add_bot(self, bot, pause_time):
        self.bots.append((bot, pause_time))

class Sitemap:
    def __init__(self, xml_file):
        self.urls = self.extract_links(self.get_xml_soup(xml_file))
    
    def get_xml_soup(self, xml_file):
        with open(xml_file) as file:
            source = file.read()
        soup = BeautifulSoup(source, 'lxml')
        return soup
    
    def __iter__(self):
        for url in self.urls:
            yield url
    
    def extract_links(self, soup):
        link_tags = soup.findAll('loc')
        links = [link_tag.text for link_tag in link_tags]
        return links

    

if __name__ == "__main__":
    logging.basicConfig(filename="logs.log")
    bot1_sitemaps = ["./kg_sitemaps/sitemap-1.xml", "./kg_sitemaps/sitemap-2.xml", "./kg_sitemaps/sitemap-3.xml"]
    bot1 = Bot(bot1_sitemaps, 1, GK_parser)
    masterbot = MasterBot([bot1])
    masterbot.run()