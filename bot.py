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
        self.sitemaps_files = sitemaps
        self.sitemap = self.get_current_sitemap() 
        self.time_of_last_request = time.time()
        self.id = Bot.BOT_ID_COUNTER
        Bot.BOT_ID_COUNTER += 1
    
    def get_current_sitemap(self):
        for sitemap_file in self.sitemaps_files:
            try:
                sitemap = Sitemap(sitemap_file)
                yield sitemap
            except:
                pass

        raise AssertionError("End of sitemaps")
        

    def parse(self, url):
        try:
            site = self.parser(url)
            data = site.get_data_dictionary()
        except ConnectionError:
            # TODO turn this into logging
            pass
        except TypeError:
            pass
        except Exception as e:
            # TODO turn this into log file
            print(e)

    
    def publish(self, data_dict):
        # TODO establish a method of publishing
        pass
    
    def add_sitemap_file(self, file):
        self.sitemaps_files.append(file)

    def get_url(self):
        while True:
            try:
                url = next(self.sitemap)
            except StopIteration:
                self.sitemap = self.get_current_sitemap()
            except Exception as e:
                # TODO turn this into log file
                print(e)
    
    def force_pause(self, pause_time):
        while (time.time() - self.time_of_last_request) < pause_time:
            time.sleep(0.05)
    
    def run(self):
        self.force_pause(self.pause_time)
        url = self.get_url()
        data_dict = self.parse(url)
        self.time_of_last_request = time.time()
        self.publish(data_dict)

class MasterBot:
    def __init__(self, bots):
        self.bots = []
        self.schedule = Schedule(self.bots)
    
    def add_bot(self, sitemaps, pause_time, parser):
        new_bot = Bot(sitemap, pause_time, parser)
        self.bots.append(new_bot)
        self.schedule = Schedule(self.bots)
    
    def remove_bot(self, bot):
        for bot_object, pause_time in self.bots:
            if bot_object == bot:
                self.bots.remove(bot)
                self.schedule = Schedule(self.bots)
                return
        else:
            raise ValueError

    def run(self):
        bot, pause_time = next(self.schedule)
        bot.run()
        time.sleep(pause_time)
    
    def run_bot(self, bot):
        try:
            self.bot.run()
        except AssertionError:
            self.remove_bot(bot)
            self.run()
        except Exception as e:
            # TODO log exception
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
