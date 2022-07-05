from session_scrape import ScraperSession
from anilist import Anilist
import timeit
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from dataclasses import dataclass

def create_log_file(data):
    with open('log.txt', 'a') as file:
        file.write(f"{data}\n")


@dataclass
class Anime:
    """
        Esta classe instancia e tipa os dados que serão manipulados pelo scraper
    """
    title_crunchyroll:str
    title_original:str
    is_dubedd: bool
    episodes:int
    duration: int
    season: str
    genres_cr: List[str]
    genres_al: List[str]
    distribuition: str
    rating_distribuition_cr: List[Dict[str,float]]
    rating_distribuition_al: List[Dict[str,float]]
    votes_cr: int
    votes_al: int
    studios: str
    source: str
    media: str
    image: str
    epi_score_dst: List[Dict[str, Any]]
    al_sequels: List[Dict[str, Any]]


class ScrapePage(ScraperSession):
    """ Estrai dados das paginas dos animes na Crunchyroll e cruza com dados do site Anilist """
    
    def __init__(self):
        super().__init__()
    
    def get_page_data(self, pages: List[str]):
        animes = []
        for index, i in enumerate(pages):
            start = timeit.default_timer()
            print(i)
            req = self.scraper.get(i)
            if req.status_code != 200:
                create_log_file(f"Error: {req.status_code} -> index: {index} -> url: {i} -> {self.__class__.__name__} -> def.get_page_data")
                return -1
            
            soup = BeautifulSoup(req.text, "html.parser")
            name_cr = self.get_name(soup)
            is_dubedd = self.is_dubedd(soup)
            genres_cr, publisher = self.get_genres(soup)
            rating_distribuition_cr, votes_cr = self.get_rating_distribuition(soup)
            anilist_data = self.get_anilist(name_cr)
            if anilist_data == -1:
                create_log_file(f"Anilist error: {name_cr} -> index: {index} -> url: {i} -> {self.__class__.__name__} -> def.get_page_data")
                return -1
            epi_score_handler = VideosData(f"{i}/videos")
            epi_scores = epi_score_handler.get_video_info()
            []
            anime = Anime(
                name_cr,
                anilist_data[0],
                is_dubedd,
                anilist_data[1],
                anilist_data[2],
                anilist_data[3],
                genres_cr,
                anilist_data[4],
                publisher,
                rating_distribuition_cr,
                anilist_data[5],
                votes_cr,
                anilist_data[6],
                anilist_data[7],
                anilist_data[8],
                anilist_data[9],
                anilist_data[10],
                epi_scores,
                anilist_data[11]             
            )
            animes.append(anime.__dict__)
            stop = timeit.default_timer()
            create_log_file(f"Success: {index + 1} de {len(pages)} -> {(((index+1) * 100) / len(pages)):.2f}% ~~{(stop - start):.2f}")

        return animes

    
    def get_genres(self, soup):
        genres = []
        publisher = []
        ul = soup.find_all("ul", id="sidebar_elements")
        for li in ul:
            a = li.find_all("a", class_="text-link")
            for item in a:
                if "genres" in str(item):
                    genres.append(item.text)
                if "publisher" in str(item):
                    publisher.append(item.text)
                    
        return genres, publisher
    
    def get_rating_distribuition(self, soup):
        ul = soup.find("ul", class_="rating-histogram")
        rating = [
            ul.find("li", class_="5-star"),
            ul.find("li", class_="4-star"),
            ul.find("li", class_="3-star"),
            ul.find("li", class_="2-star"),
            ul.find("li", class_="1-star")
        ]
        data = []
        for index, rt in enumerate(rating[::-1]):
            for on in rt.find_all("div",class_="left"):
                if "left" in str(on):
                    if "num" not in str(on) and "rating" not in str(on):
                        if on.text.replace("(", "").replace(")", "") != "":
                            data.append({"score": index+1, "amount": int(on.text.replace("(", "").replace(")", ""))})
                        else:
                            data.append({"score": index+1, "amount": 0})
                        
        return data, sum([i["amount"] for i in data])
    
    
    def get_anilist(self, title):
        anilist = Anilist(title)
        data = anilist.response_handle()
        if len(data) == 1:
            original_title = data[0]["title"]["romaji"]
            episodes_number = data[0]["episodes"]
            episodes_duration = data[0]["duration"]
            source = data[0]["source"]
            media = data[0]["format"]
            season = data[0]["season"]
            image = data[0]["coverImage"]["large"]
            rating_distribuition = data[0]["stats"]["scoreDistribution"]
            votes_al = sum([i["amount"] for i in data[0]["stats"]["scoreDistribution"]])
            studios = data[0]["studios"]["edges"]
            genres_anilist = data[0]["genres"]
            relations_data = data[0]["relations"]["edges"]
            
            return [
                original_title,
                episodes_number,
                episodes_duration,
                season,
                genres_anilist,
                rating_distribuition,
                votes_al,
                studios,
                source,
                media,
                image,
                relations_data]
        
        
        return [None for i in range(13)]
    
    def is_dubedd(self, soup):
        a = soup.find_all("a", class_="season-dropdown content-menu block text-link strong small-margin-bottom")
        
        if "Portuguese Dub" in str(a):
            return True
        if "Dub PT" in str(a):
            return True
        
        return False
    
    def get_name(self, soup):
        div = soup.find("h1", class_="ellipsis")
        
        name = div.find("span").text
        return name


class VideosData(ScraperSession):
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.urls_videos, self.videos_count = self.get_videos_data()
    
    def get_videos_data(self):
        req = self.scraper.get(self.url)
        print(":-> ", self.url)
        if req.status_code != 200:
            create_log_file(f"Error: {req.status_code} -> url: {self.url} -> {self.__class__.__name__}")
            return -1
        
        soup = BeautifulSoup(req.text, "html.parser")
        uls = soup.find_all("ul", class_="portrait-grid cf")
        
        for ul in uls:
            if 'style=""' in str(ul):
                lis = ul.find_all("li")
                episodes = len(lis)
                links = []
                for li in lis:
                    a = li.find("a", class_="episode")
                    links.append(f'https://www.crunchyroll.com{a.get("href")}')
                return (links, episodes)

            elif 'style=""' not in str(ul):
                a_ = soup.find_all("a", class_="portrait-element block-link titlefix episode")
                links = [f'https://www.crunchyroll.com{a["href"]}' for a in a_]
                return (links, len(links))
        
                
    
    def get_video_info(self) -> List[Dict[str,Any]]:
        resp = []
        
        for index, url in enumerate(self.urls_videos):

            req = self.scraper.get(url)
            if req.status_code != 200:
                create_log_file(f"Error: {req.status_code} -> index: {index} -> url: {url} -> {self.__class__.__name__}")
                return -1
            
            soup = BeautifulSoup(req.text, "html.parser")
            votes = soup.find("div", id="showmedia_about_sampleSizeText")
            votes_span = votes.find("span")
            
            episode = soup.find("div", id="showmedia_about_media")
            episode_h4 = episode.find_all("h4")[-1]
            
            span = soup.find("span", id="showmedia_about_rate_widget")
            rating = str(span).split("Rating.SetStars")[1].split(",")[0]
            
            resp.append({"episode": episode_h4.text.strip(), "rating": float(rating.replace("(","")), "votes": int(votes_span.text)})
        
        return resp
            

