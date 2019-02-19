import requests
from bs4 import BeautifulSoup
import json
import pprint

class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(url)

    def get_soup(self, url):
        try:
            html_source = requests.get(url).text
            soup = BeautifulSoup(html_source, 'lxml')
        except:
            raise ConnectionError
        return soup
    
    def try_catch_getter(function):
        def wrapper(*args):
            try:
                value =  function(*args)
                return value
            except:
                return None

        return wrapper

    
    def get_data_dictionary(self):
        data = dict()

        # TODO turn this into SQLAlchemy or CSV
        data["name"] = self.get_name()
        data["url"] = self.get_url()
        data["ingredients"] = self.get_ingredients()
        data["directions"] = self.get_directions()
        data["rating"] = self.get_rating()
        data["img_link"] = self.get_img_link()
        data["categories"] = self.get_categories()
        data["time"] = self.get_time()
        data["publisher"] = self.get_publisher()
        data["meta"] = self.get_meta()
        data["food_yield"] = self.get_yield()
        data["description"] = self.get_description()
        data["reviews"] = self.get_reviews()

        return data


class JSON_schema(Parser):
    def __init__(self, url):
        super().__init__(url)
        self.json_data = self.get_json_data(self.soup)

    def get_json_data(self, soup):
        # KG has most data stored in a json section that can be parsed
        try:
            json_text = soup.find('script', type = "application/ld+json").text
        except:
            raise TypeError ("Does not include JSON")

        data = json.loads(json_text)
        return data 
    
    
    @Parser.try_catch_getter
    def get_ingredients(self):
        # returns a list of ingredients unformatted 
        ingredient_list = self.json_data["recipeIngredient"]
        return ingredient_list
    
    @Parser.try_catch_getter
    def get_directions(self):
        # returns a list of directions in order
        direction_dict_formated = self.json_data["recipeInstructions"]
        direction_list = [item["text"] for item in direction_dict_formated]
        return direction_list
    
    @Parser.try_catch_getter
    def get_img_link(self):
        # returns a link to the img source 
        img_link = self.json_data["image"]
        return img_link
    
    @Parser.try_catch_getter
    def get_url(self):
        # returns a link as a string
        return self.url
    
    @Parser.try_catch_getter
    def get_name(self):
        # returns the name as a string
        name = self.json_data["name"]
        return name

    @Parser.try_catch_getter
    def get_nutrition(self):
        # returns a dictionary of nutrition values
        nutrition = self.json_data["nutrition"]
        del nutrition["@type"]
        return nutrition
    
    @Parser.try_catch_getter
    def get_time(self):
        # returns a tuple in the format (prep_time, cooking_time, total_time)
        prep_time = self.json_data["prepTime"]
        cooking_time = self.json_data["cookTime"]
        total_time = self.json_data["totalTime"]
        return prep_time, cooking_time, total_time
    
    @Parser.try_catch_getter
    def get_publisher(self):
        # returns the publisher name as a string
        publisher = self.json_data["publisher"]["name"]
        return publisher
    
    @Parser.try_catch_getter
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

    @Parser.try_catch_getter
    def get_yield(self):
        # returns the number of servings as a string
        recipe_yield = self.json_data["recipeYield"]
        return recipe_yield
    
    @Parser.try_catch_getter
    def get_description(self):
        # returns a description of the food 
        description = self.json_data["description"]
        return description
    
    @Parser.try_catch_getter
    def get_reviews(self):
        # returns a list of reviews it can find on the page
        top_review = self.json_data["review"][0]["description"]
        return [top_review]
    
    @Parser.try_catch_getter
    def get_categories(self):
        # returns a list of categories
        main_category = self.json_data["recipeCategory"]
        keywords = self.json_data["keywords"].split(",")
        category_list = [main_category] + keywords
        return category_list
    


class GK_parser(JSON_schema):
    def __init__(self, url):
        super().__init__(url)
    
    @Parser.try_catch_getter
    def get_rating(self):
        # returns tuple in the format of (rating, # ratings)
        review_count = int(self.json_data["aggregateRating"]["reviewCount"])
        rating = float(self.soup.find("span", class_="sr-only").text)
        return rating, review_count
    
    @Parser.try_catch_getter
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
        # clean categories by removing redandant categories and sepate combined categories
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

class HTML_schema(Parser):
    def __init__(self, url):
        super().__init__(url)
    
    @Parser.try_catch_getter
    def get_ingredients(self):
        # returns a list of ingredients unformatted
        ingredient_tags = self.soup.findAll("span", attrs = {"itemprop" : "recipeIngredient"})
        ingredients = [ingredient_tag.text for ingredient_tag in ingredient_tags]
        return ingredients
    
    @Parser.try_catch_getter
    def get_directions(self):
        # returns a list of directions in order
        direction_tags = self.soup.findAll("span", class_ ="recipe-directions__list--item")
        directions = [direction_tag.text for direction_tag in direction_tags]
        return directions
    
    @Parser.try_catch_getter
    def get_rating(self):
        # returns tuple in the format of (rating, rating_count)
        rating_tag = self.soup.find("meta", attrs = {"itemprop" : "ratingValue"})
        rating = float(rating_tag["content"])
        rating_count_tag = self.soup.find("meta", attrs = {"itemprop" : "reviewCount"})
        rating_count = int(rating_count_tag["content"])
        return rating, rating_count

    @Parser.try_catch_getter
    def get_categories(self):
        # returns a list of categories
        category_tags = self.soup.findAll("meta", {"itemprop" : "recipeCategory"})
        categories = [category_tag["content"] for category_tag in category_tags]
        cuisines = self.get_cuisines()
        all_categories = cuisines + categories
        return all_categories
    
    @Parser.try_catch_getter
    def get_cuisines(self):
        cuisine_tags = self.soup.findAll("meta", {"itemprop" : "recipeCuisine"})
        cuisines = [cuisine_tag["content"] for cuisine_tag in cuisine_tags]
        return cuisines
    
    @Parser.try_catch_getter
    def get_link(self):
        # returns a link as a string
        return self.url
    
    @Parser.try_catch_getter
    def get_name(self):
        # returns the name as a string
        name_tag = self.soup.find("h1", {"itemprop" : "name"})
        name = name_tag.text
        return name

    @Parser.try_catch_getter
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
    
    @Parser.try_catch_getter
    def get_time(self):
        # returns a tuple in the format (prep_time, cooking_time, total_time)
        prep_time = self.soup.find("time", {"itemprop" : "prepTime"})["datetime"]
        cooking_time = self.soup.find("time", {"itemprop" : "cookTime"})["datetime"]
        total_time = self.soup.find("time", {"itemprop" : "totalTime"})["datetime"]
        return prep_time, cooking_time, total_time
    
    @Parser.try_catch_getter
    def get_publisher(self):
        # returns the publisher name as a string
        publisher_tag = self.soup.find("meta", attrs={"property":"og:site_name"})
        publisher = publisher_tag["content"]
        return publisher

    @Parser.try_catch_getter
    def get_yield(self):
        # returns the number of servings as a string
        recipe_yield_tag = self.soup.find("meta", attrs={"itemprop" : "recipeYield"})
        recipe_yield = recipe_yield_tag["content"]
        return recipe_yield
    
    @Parser.try_catch_getter
    def get_description(self):
        # returns a description of the food 
        description_tag = self.soup.find("meta", attrs={"id" : "metaDescription"})
        description = description_tag["content"]
        return description
    
    @Parser.try_catch_getter
    def get_url(self):
        return self.url
    
    # TODO fix this
    @Parser.try_catch_getter
    def get_img_link(self):
        pass
    
    # TODO fix this
    @Parser.try_catch_getter
    def get_meta(self):
        pass
    
    @Parser.try_catch_getter
    def get_reviews(self):
        return []

class AR_parser(HTML_schema):
    # TODO remove the html_sources
    def __init__(self, html_source):
        super().__init__(html_source)
    
    @Parser.try_catch_getter
    def get_directions(self):
        raw_directions = super().get_directions()
        cleaned_directions = self.clean_directions(raw_directions)
        return cleaned_directions
    
    def clean_directions(self, directions):
        directions = [direction.split("\n") for direction in directions]
        directions = [direction[0] for direction in directions if len(direction) > 1]
        return directions
    
    @Parser.try_catch_getter
    def get_reviews(self):
        # returns a list of reviews it can find on the page
        review_data = json.loads(self.get_review_json())["reviews"]["Reviews"]
        reviews = [review["text"] for review in review_data]
        return reviews

    def get_review_json(self):
        json_section = self.soup.find("section", class_="ar_recipe_index full-page")
        scripts = json_section.findAll("script")
        json_data = [script.text for script in scripts][-2][30:-3]
        return json_data
    
if __name__ == "__main__":
    url_real = "https://www.geniuskitchen.com/recipe/the-best-easy-beef-and-broccoli-stir-fry-99476"
    url_broken = "https://www.allrecipes.com/recipe/45957/chicken-makhani-indian-butter-chicken/?clickId=right%20rail1&internalSource=rr_feed_recipe_sb&referringId=73021%20referringContentType=recipe"
    test_url = "https://www.bbcgoodfood.com/recipes/slow-cooker-lamb-curry"
    test_2_url = "https://www.epicurious.com/recipes/member/views/microwave-peppy-parmesan-potatoes-1270209"
    parser = HTML_schema(test_2_url)
    data = parser.get_data_dictionary()
    printer = pprint.PrettyPrinter()
    printer.pprint(data)