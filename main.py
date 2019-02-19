from GzSitemapDir import gz_sitemap_dir_download
from bot import MasterBot, Bot
from parser import GK_parser

def main():
    KG_sitemaps = gz_sitemap_dir_download("https://www.geniuskitchen.com/sitemap.xml", 1.0, "test_file")
    KG_bot = Bot(KG_sitemaps, 1.0, GK_parser)
    Controller = MasterBot([KG_bot])
    Controller.run()

if __name__ == "__main__":
    main()