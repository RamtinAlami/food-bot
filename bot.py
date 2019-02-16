import csv
import requests
from bs4 import BeautifulSoup
import time
import json

# NEED TO IMPLEMENT A START AND END SO SMALLER SECTIONS CAN BE PARSED
class bot:
    def __init__(self, sitemaps):
        pass

class KG_agent(bot):
    def __init__(self, sitemap):
        pass

class RR_agent(bot):
    def __init__(self, sitemap):
        pass

class KG_parser:
    def __init__(self, html_source):
        # html source is str of text of page
        # NEED TO ADD LINK HERE INSTEAD OF TEXT
        self.url = "will be added"
        self.soup = BeautifulSoup(html_source, 'lxml')
        self.json_data = self.get_json_data(self.soup)

    def get_json_data(self, soup):
        # KG has most data stored in a json section that can be parsed
        json_text = soup.find('script', type = "application/ld+json").text
        data = json.loads(json_text)
        return data 
    
    def get_ingredients(self):
        # returns a list of ingredients unformatted 
        ingredient_list = self.json_data["recipeIngredient"]
        return ingredient_list
    
    def get_directions(self):
        # returns a list of directions in order
        direction_dict_formated = self.json_data["recipeInstructions"]
        direction_list = [item["text"] for item in direction_dict_formated]
        return direction_list
    
    def get_img_link(self):
        # returns a link to the img source 
        img_link = self.json_data["image"]
        return img_link

    def get_rating(self):
        # returns tuple in the format of (rating, # ratings)
        review_count = int(self.json_data["aggregateRating"]["reviewCount"])
        rating = float(self.soup.find("span", class_="sr-only").text)
        return rating, review_count

    def get_categories(self):
        # returns a tuple of categories
        """

        THIS NEEDS MORE WORK AND THE CATEGORIES NEED BE DOUBLE CHECKED
        FOR THE VALIDY OF THEM 

        """
        main_category = self.json_data["recipeCategory"]
        keywords = self.json_data["keywords"].split(",")
        category_list = [main_category] + keywords
        return category_list
    
    def get_url(self):
        # returns a link as a string
        return self.url
    
    def get_name(self):
        # returns the name as a string
        name = self.json_data["name"]
        return name

    def get_nutrition(self):
        # returns a dictionary of nutrition values
        nutrition = self.json_data["nutrition"]
        del nutrition["@type"]
        return nutrition
    
    def get_time(self):
        # returns a tuple in the format (prep_time, cooking_time, total_time)
        prep_time = self.json_data["prepTime"]
        cooking_time = self.json_data["cookTime"]
        total_time = self.json_data["totalTime"]
        return prep_time, cooking_time, total_time
    
    def get_publisher(self):
        # returns the publisher name as a string
        publisher = self.json_data["publisher"]["name"]
        return publisher
    
    def get_meta(self):
        # returns a tuple with (author name, date published)
        author_name = self.json_data["author"]
        date_published = self.json_data["datePublished"]
        # need to fix data to dictionary of year, day, month
        return author_name, date_published

    def get_yield(self):
        # returns the number of servings as a string
        recipe_yield = self.json_data["recipeYield"]
        return recipe_yield
    
    def get_description(self):
        # returns a description of the food 
        description = self.json_data["description"]
        return description
    
    def get_reviews(self):
        # returns a list of reviews it can find on the page
        top_review = self.json_data["review"][0]["description"]
        return [top_review]
    
    def test(self):
        print(self.get_reviews())
    

class RR_parser:
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



if __name__ == "__main__":
    with open("KG_sample.html") as sample_html:
        html_source = sample_html.read()

    parser = KG_parser(html_source)
    parser.test()
    
