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
    
    def pretty_print(self):
        url = self.get_url()
        name = self.get_name()
        ingredients = self.get_ingredients()
        directions = self.get_directions()
        rating = self.get_rating()
        img_link = self.get_img_link()
        categories = self.get_categories()
        time = self.get_time()
        publisher = self.get_publisher()
        meta = self.get_meta()
        food_yield = self.get_yield()
        description = self.get_description()
        reviews = self.get_reviews()

        print(
            f"""Website : {url}

            Img : {img_link}

            Publisher : {publisher}

            Name : {name}

            Meta : {meta}

            Categories : {categories}

            Rating : {rating}

            Cook time : {time}

            Yield : {food_yield}

            Description : {description}

            Ingredients : {ingredients}

            Directions : {directions}

            Reviews : {reviews}
            """
        )


class JSON_schema(Parser):
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

    def get_categories(self):
        # returns a tuple of categories
        # removes time categories as can be recalculated
        # removes buffer categories 
        # separates mix categories
        # TODO there are more things to add such as cuisine 
        main_category = self.json_data["recipeCategory"]
        keywords = self.json_data["keywords"].split(",")
        category_list = [main_category] + keywords
        self.clean_categories(category_list)
        return category_list

    def clean_categories(self, input_list):
        # clean categories 
        remove_item_list = ['Time To Make', 'High In...']
        remove_item_list += [self.find_time_item(input_list)]
        self.separate_sub_categories(input_list)
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
    
    def separate_sub_categories(self, input_list):
        # separates mix categories such as "Heirloom/Historical" to 2 separates categories
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


class GK_parser(JSON_schema):
    def __init__(self, url):
        super().__init__(url)
    
    def get_rating(self):
        # returns tuple in the format of (rating, # ratings)
        review_count = int(self.json_data["aggregateRating"]["reviewCount"])
        rating = float(self.soup.find("span", class_="sr-only").text)
        return rating, review_count

    def get_reviews(self):
        # returns a list of reviews it can find on the page
        pass

class HTML_schema:
    def __init__(self, html_source, url):    
        #TODO remove the html_source and convert to URL retrival
        with open(html_source) as source:
            self.source = source.read()

        self.soup = BeautifulSoup(self.source, 'lxml') 
        self.url = url
    
    def get_ingredients(self):
        # returns a list of ingredients unformatted 
        ingredient_tags = self.soup.findAll("span", attrs = {"itemprop" : "recipeIngredient"})
        ingredients = [ingredient_tag.text for ingredient_tag in ingredient_tags]
        return ingredients
    
    def get_directions(self):
        # returns a list of directions in order
        direction_tags = self.soup.findAll("span", class_ ="recipe-directions__list--item")
        directions = [direction_tag.text for direction_tag in direction_tags]
        return directions
    
    def get_rating(self):
        # returns tuple in the format of (rating, rating_count)
        rating_tag = self.soup.find("meta", attrs = {"itemprop" : "ratingValue"})
        rating = float(rating_tag["content"])
        rating_count_tag = self.soup.find("meta", attrs = {"itemprop" : "reviewCount"})
        rating_count = int(rating_count_tag["content"])
        return rating, rating_count

    def get_categories(self):
        # returns a list of categories
        category_tags = self.soup.findAll("meta", {"itemprop" : "recipeCategory"})
        categories = [category_tag["content"] for category_tag in category_tags]
        cuisines = self.get_cuisines()
        all_categories = cuisines + categories
        return all_categories
    
    def get_cuisines(self):
        cuisine_tags = self.soup.findAll("meta", {"itemprop" : "recipeCuisine"})
        cuisines = [cuisine_tag["content"] for cuisine_tag in cuisine_tags]
        return cuisines
    
    def get_link(self):
        # returns a link as a string
        return self.url
    
    def get_name(self):
        # returns the name as a string
        name_tag = self.soup.find("h1", {"itemprop" : "name"})
        name = name_tag.text
        return name

    def get_nutrition(self):
        # returns a dictionary of nutrition values
        nutritions = dict()
        nutritions["calories"] = self.soup.find("span", {"itemprop" : "calories"}).text
        nutritions["fatContent"] = float(self.soup.find("span", {"itemprop" : "fatContent"}).text)
        nutritions["carbohydrateContent"] = float(self.soup.find("span", {"itemprop" : "carbohydrateContent"}).text)
        nutritions["proteinContent"] = float(self.soup.find("span", {"itemprop" : "proteinContent"}).text)
        nutritions["cholesterolContent"] = float(self.soup.find("span", {"itemprop" : "cholesterolContent"}).text)
        nutritions["sodiumContent"] = float(self.soup.find("span", {"itemprop" : "sodiumContent"}).text)
        return nutritions
    
    def get_time(self):
        # returns a tuple in the format (prep_time, cooking_time, total_time)
        prep_time = self.soup.find("time", {"itemprop" : "prepTime"})["datetime"]
        cooking_time = self.soup.find("time", {"itemprop" : "cookTime"})["datetime"]
        total_time = self.soup.find("time", {"itemprop" : "totalTime"})["datetime"]
        return prep_time, cooking_time, total_time
    
    def get_publisher(self):
        # returns the publisher name as a string
        publisher_tag = self.soup.find("meta", attrs={"property":"og:site_name"})
        publisher = publisher_tag["content"]
        return publisher

    def get_yield(self):
        # returns the number of servings as a string
        recipe_yield_tag = self.soup.find("meta", attrs={"itemprop" : "recipeYield"})
        recipe_yield = recipe_yield_tag["content"]
        return recipe_yield
    
    def get_description(self):
        # returns a description of the food 
        description_tag = self.soup.find("meta", attrs={"id" : "metaDescription"})
        description = description_tag["content"]
        return description
    
    def get_reviews(self):
        return []
    
    def test(self):
        data = self.get_reviews()
        print(data)

class AR_parser(HTML_schema):
    # TODO remove the html_sources
    def __init__(self, html_source, url):
        super().__init__(html_source, url)
    
    def get_directions(self):
        raw_directions = super().get_directions()
        cleaned_directions = self.clean_directions(raw_directions)
        return cleaned_directions
    
    def clean_directions(self, directions):
        directions = [direction.split("\n") for direction in directions]
        directions = [direction[0] for direction in directions if len(direction) > 1]
        return directions
    
    def get_reviews(self):
        # returns a list of reviews it can find on the page
        review_data = json.loads(self.get_review_json())["reviews"]["Reviews"]
        reviews = [review["text"] for review in review_data]
        return reviews

    def get_review_json(self):
        script_tags = self.soup.findAll("script")
        script_list = [script_tag.text for script_tag in script_tags if script_tag]
        json_data = [script for script in script_list if script[:26] == "\n    var reviewsInitialSet" ][0][29:-2]
        return json_data
    


if __name__ == "__main__":
    html_source = "AR_sample.html"
    parser = AR_parser(html_source, "www")
    parser.test()
    
