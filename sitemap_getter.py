import requests
from bs4 import BeautifulSoup
import gzip
import time
import urllib.request
import os


sitemaps = requests.get("https://www.foodnetwork.com/sitemaps/sitemap_food_index.xml").text
soup = BeautifulSoup(sitemaps, 'lxml')
sitemaps_url_tags = soup.findAll("loc")
sitemaps_urls = [sitemap_tag.text for sitemap_tag in sitemaps_url_tags]

for sitemap_url in sitemaps_urls:
    time.sleep(1)
    file_name = sitemap_url.split("/")[-1]
    print(file_name)
    gz_file, headers = urllib.request.urlretrieve(sitemap_url, file_name)
    with gzip.open(gz_file, 'rb') as f:
        content = f.read()
    xml_file_name = file_name[:-3]
    print(xml_file_name)

    with open(xml_file_name, "bw") as xml_file:
        xml_file.write(content)    
    
    os.system(f"rm {gz_file}")
    os.system(f"mv {xml_file_name} fn_sitemaps/{xml_file_name}")