import csv
import requests
from bs4 import BeautifulSoup
import time
import json

class bot:
    def __init__(self, sitemaps):
        pass

class KG_agent(bot):
    def __init__(self, sitemap):
        pass

class RR_agent(bot):
    def __init__(self, sitemap):
        pass

class KG_parser(KG_agent):
    def __init__(self, html_source):
        pass
    
    def get_ingredients(self):
        # returns a list of ingredients unformatted 
        pass
    
    def get_directions(self):
        # returns a list of directions in order
        pass

    def get_rating(self):
        # returns tuple in the format of (rating, # ratings)
        pass

    def get_categories(self):
        # returns a tuple of categories
        pass
    
    def get_link(self):
        # returns a link as a string
        pass
    
    def get_name(self):
        # returns the name as a string
        pass

    def get_nutrition(self):
        # returns a dictionary of nutrition values
        pass
    
    def get_time(self):
        # returns a tuple in the format (prep_time, cooking_time)
        pass
    
    def get_publisher(self):
        # returns the publisher name as a string
        pass

    def get_yield(self):
        # returns the number of servings as a string
        pass
    
    def get_description(self):
        # returns a description of the food 
        pass
    
    def get_reviews(self):
        # returns a list of reviews it can find on the page
        pass

class RR_parser(RR_agent):
    def __init__(self, html_source):
        pass
    
    def get_ingredients(self):
        # returns a list of ingredients unformatted 
        pass
    
    def get_directions(self):
        # returns a list of directions in order
        pass

    def get_rating(self):
        # returns tuple in the format of (rating, # ratings)
        pass

    def get_categories(self):
        # returns a tuple of categories
        pass
    
    def get_link(self):
        # returns a link as a string
        pass
    
    def get_name(self):
        # returns the name as a string
        pass

    def get_nutrition(self):
        # returns a dictionary of nutrition values
        pass
    
    def get_time(self):
        # returns a tuple in the format (prep_time, cooking_time)
        pass
    
    def get_publisher(self):
        # returns the publisher name as a string
        pass

    def get_yield(self):
        # returns the number of servings as a string
        pass
    
    def get_description(self):
        # returns a description of the food 
        pass
    
    def get_reviews(self):
        # returns a list of reviews it can find on the page
        pass
