import requests
import cfscrape

user_agent = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
]
cookie = 'cole os cookies do site, voce pode conceguilos usando a ferramenta de desenvolvedor do navegador na aba de Network/rede, necessita estar logado no site pois alguns animes são bloquados para menores.'


class ScraperSession:
    """ Esta classe cria uma sessão e inicia o cfscrape com essa sessão.
        É necessário para passar pelo bloqueio do cloudflare.
    """
    
    def __init__(self):
        session = requests.Session()
        session.headers = {'cookie': cookie}
        self.scraper = cfscrape.create_scraper(sess=session)