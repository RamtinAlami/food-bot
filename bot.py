import csv
import requests
from bs4 import BeautifulSoup
import time
import json

# NEED TO IMPLEMENT A START AND END SO SMALLER SECTIONS CAN BE PARSED
class Bot:
    def __init__(self, sitemaps):
        pass

class KG_agent(Bot):
    def __init__(self, sitemap):
        pass

class RR_agent(Bot):
    def __init__(self, sitemap):
        pass

class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(url)

    def get_soup(self, url):
        try:
            html_source = requests.get(url).text
            soup = BeautifulSoup(html_source, 'lxml')
        except:
            # NEEDS TO BE HANDLED THE CALLER TO SKIP AND GO TO NEXT url link
            raise ConnectionError
        return soup

class KG_parser(Parser):
    def __init__(self, url):
        super().__init__(url)
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
        # removes time categories as can be recalculated
        # removes buffer categories 
        # seperates mix categories
        main_category = self.json_data["recipeCategory"]
        keywords = self.json_data["keywords"].split(",")
        category_list = [main_category] + keywords
        self.clean_categories(category_list)
        return category_list
    
    def clean_categories(self, input_list):
        # clean categories 
        remove_item_list = ['Time To Make', 'High In...']
        remove_item_list += [self.find_time_item(input_list)]
        self.sepreate_sub_categories(input_list)
        for item in remove_item_list:
            self.try_remove(input_list, item)
    
    def find_time_item(self, input_list):
        # given a category list, returns the time item to be removed
        time_item = None
        for item in input_list:
            if item[0] == "<":
                time_item = item
                break
        return time_item
    
    def sepreate_sub_categories(self, input_list):
        # seperate mix categories such as "Heirloom/Historical" to 2 seperate categories
        seperatable = [item for item in input_list if len(item.split("/")) > 1]
        for item in seperatable:
            self.try_remove(input_list, item) # remove mix
            input_list += item.split("/") # add items as individuals

    def try_remove(self, input_list, item):
        # goes through a list and tries to remove the item if present
        try:
            input_list.remove(item)
        except:
            pass
    
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
        # returns a tuple with (author name, date published <dictionary>)
        author_name = self.json_data["author"]
        date_published = self.json_data["datePublished"]
        formated_date = self.format_date(date_published)
        return author_name, formated_date
    
    def format_date(self, date_string):
        try:
            date = date_string.split("T")[0]
            date = date.split("-")
            output_date = {"year":date[0], "month":date[1], "day":date[2]}
        except:
            output_date = date_string

        return output_date

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
    parser = KG_parser("https://www.geniuskitchen.com/recipe/beths-melt-in-your-mouth-barbecue-ribs-oven-107786")
    parser.test()
    
