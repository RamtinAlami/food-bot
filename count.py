import os
from bs4 import BeautifulSoup

count = 0
MAPS_PATH = "./kg_sitemaps"
files = os.listdir(MAPS_PATH)
files = [MAPS_PATH + "/" + xml_file for xml_file in files]
for xml_file_name in files:
    with open(xml_file_name) as xml_file:
        source = xml_file.read()
    soup = BeautifulSoup(source, 'lxml')
    tags = soup.findAll("loc")
    count += len(tags)
    with open(xml_file_name, "w") as xml_file:
        for tag in tags:
            xml_file.write(f"<loc>{tag.text}</loc>\n")

print(count)
