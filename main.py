from bs4 import BeautifulSoup
import requests

from session_scrape import ScraperSession
from scraper_page import ScrapePage

def file_create(file, name):
    with open(f"{name}", "w", encoding="utf-8") as f:
            f.write(file)


def get_robots(url: str):
    robots_roles = requests.get(f"{url}/robots.txt")
    try:
        with open("robots.txt", "w") as f:
            f.write(robots_roles.text)
    except Exception as e:
        return print(e)
    
    return print("Arquivo robots.txt gerado com sucesso!")


class UrlPageBuilder(ScraperSession):
    """Cria uma lista com as urls dos animes para extração dos dados"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.crunchyroll.com"
        self.all_animes = "https://www.crunchyroll.com/pt-br/videos/anime/alpha?group=all"
    
    def get_page_links(self):
       req = self.scraper.get(self.all_animes)
       soup = BeautifulSoup(req.text, "html.parser")
       a = soup.find_all("a", token="shows-portraits")
       return [f'{self.base_url}{i["href"]}' for i in a]
    

if __name__ == "__main__":

    url_page_builder = UrlPageBuilder()
    page_urls = url_page_builder.get_page_links()
   
    page_scraper = ScrapePage()
    data = page_scraper.get_page_data(page_urls)
