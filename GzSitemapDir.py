import requests
from bs4 import BeautifulSoup
import gzip
import time
import urllib.request
import os

class GzSitemapDir:
    def __init__(self, sitemap_dir_url, server_pause_time):
        self.sitemap_dir_url = sitemap_dir_url
        self.gz_sitemap_urls = self.get_sitemaps_url()
        self.pause_time = server_pause_time
        self.sitemap_locations = []
    
    def get_sitemaps_url(self):
        sitemaps = requests.get(self.sitemap_dir_url).text
        soup = BeautifulSoup(sitemaps, 'lxml')
        sitemaps_url_tags = soup.findAll("loc")
        sitemaps_urls = [sitemap_tag.text for sitemap_tag in sitemaps_url_tags]
        return sitemaps_urls
    
    def download_sitemap(self, url):
        gz_sitemap = Gz_sitemap(url)
        gz_sitemap.download()
        gz_sitemap.unzip()
        gz_sitemap.delete_gz_file()
        return gz_sitemap.file_name
    
    def save_sitemaps(self, folder_name):
        os.mkdir(folder_name)
        for url in self.gz_sitemap_urls:
            time.sleep(self.pause_time)
            sitemap_file = self.download_sitemap(url)
            os.system(f"mv {sitemap_file} {folder_name}/{sitemap_file}")
            self.sitemap_locations.append(f"{folder_name}/{sitemap_file}")
    
    def save_files_locally(self, folder_name):
        self.save_sitemaps(folder_name)
    
    def clean_memory(self):
        for file_location in self.sitemap_locations:
            os.system(f"rm {file_location}")
        self.sitemap_locations = []
        

class Gz_sitemap:
    def __init__(self, download_link):
        self.file_name = download_link.split("/")[-1][:-3]
        self.download_link = download_link
    
    def download(self):
        gz_file, headers = urllib.request.urlretrieve(self.download_link, self.file_name + ".gz")
    
    def unzip(self):
        gz_file = self.file_name + ".gz"
        with gzip.open(gz_file, 'rb') as f:
            content = f.read()
        with open(self.file_name, "bw") as xml_file:
            xml_file.write(content)

    def delete_gz_file(self):
        os.system(f"rm {self.file_name}.gz")
    

class gz_sitemap_dir_download:
    def __init__(self, download_link, server_pause, folder_name):
        self.sitemaps = GzSitemapDir(download_link, server_pause)
        self.sitemaps.save_files_locally(folder_name)
        self.sitemap_dirs = self.sitemaps.sitemap_locations
    
    def clear(self):
        self.sitemaps.clean_memory()


if __name__ == "__main__":
    pass
    
    

