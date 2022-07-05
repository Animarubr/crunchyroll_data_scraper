# Projeto de Web Scraping do Site Crunchyroll BR

#### O objetivo do projeto é coletar dados com web scraping do site da <a target="_blank" href="https://www.crunchyroll.com/pt-br">Crunchyroll Brasil</a> para posteriormente criar projetos de Data Science, como recomendação, e previsão de popularidade com os dados.


> Dados da Crunchyroll são globais, ou seja os números de views e avaliação independe do idioma do áudio ou do país que esta sendo acessado.
> Para fins de avaliação os números serão globais, porém a base de dados será apenas de animes acessíveis no Brasil.


Para rodar o projeto basta instalar o arquivo de requirements.txt e posteriormente
usar o comando ```python main.py``` no terminal.

O script cruza os dados do site Crunchyroll com o site <a target="_blank" href="https://anilist.co/home">Anilist.co</a>, que é uma plataforma de avaliação de animes por fãs, os dados retirados foram os seguintes:

**Crunchyroll**

    title
    is_dubbed -> se é dublado em pt-br
    genres
    distribuition -> empresa responsavél pela distribuição dos animes
    rating_distribuition
    votes
    epi_score_distribuition -> distribuição de notas e votos por episódio.

**Anilist**

    title
    duration
    episode -> numero de episódios
    season -> temporada de lançamento --usam as estações do ano no hemisferio norte--
    genres
    rating_distribuition
    votes
    studios
    source -> fonte original da obra ex.: MANGA, ORIGINAL, ETC…
    media -> tipo de media ex.: TV, OVA, ETC…
    image
    sequences -> temporadas sequenciais do anime

Os dados resultantes deste projeto serão salvos em um arquivo csv para as analises e criação de modelos de Machine Learning.
