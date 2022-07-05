import requests

class Anilist:
    
    def __init__(self, name):
        self.name = name
    
    def anilist_query(self, name: str):
        
        query = """
            query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                        currentPage
                        lastPage
                        hasNextPage
                        perPage
                    }
                    media (id: $id, search: $search, type: ANIME) {
                        id
                        title {
                            romaji
                            english
                        },
                        coverImage {
                            large
                        },
                        startDate {
                            year
                        }
                        format
                        duration
                        episodes
                        season
                        source
                        synonyms
                        genres

                        stats {
                            scoreDistribution {
                                score
                                amount
                            }
                        }
                        studios{edges{isMain node{id name}}}
                        relations {
                            
                            edges {
                                relationType
                                node {
                                    id
                                    title {
                                        romaji
                                        english
                                    }
                                    coverImage {
                                        large
                                    }
                                    duration
                                    episodes
                                    season
                                    format
                                    genres
                                    startDate {
                                        year
                                    }
                                    stats {
                                        scoreDistribution {
                                            score
                                            amount
                                        }
                                    }
                                    studios{edges{isMain node{id name}}}
                                    
                                    
                                }
                            }
                        }
                                       
                    }      
                }
            }
            """

        variables = {"search": name, "page": 1, "perPage": 1}

        url = "https://graphql.anilist.co"
        resp = requests.post(url, json={"query": query, "variables": variables}).json()
        return resp


    def get_sequel(self, name):
        name_ = name
        data = []
        while True:
            dt = self.anilist_query(name_)
            if len(dt["data"]["Page"]["media"][0]) == 0:
                break
            
            dtf = [key for key in dt["data"]["Page"]["media"][0]["relations"]["edges"] if key["relationType"] == "SEQUEL"]
            dt_ = [node for node in dtf if node["node"]["duration"] is not None]
            
            for index, i in enumerate(dt_):
                
                if i["node"]["id"] in [id_["node"]["id"] for id_ in data]:
                    dt_.pop(index)
            
            if len(dt_) > 1:
                year = 0
                for el in dt_:
                    if year == 0:
                        year = el["node"]["startDate"]["year"]
                        
                    if el["node"]["startDate"]["year"] > year:
                        dt_ = [el]
                    else:
                        dt_ = [el]
            if dt_ == []:
                break
            
            for i in dt_:

                if len(data) == 0:
                    studios = [st for st in i["node"]["studios"]["edges"] if st["isMain"] == True]
                    i["node"]["studios"]["edges"] = studios
                    data.append(i)
                    name_ = i["node"]["title"]["romaji"]
                    
                if i["node"]["id"] not in [id_["node"]["id"] for id_ in data]:
                    studios = [st for st in i["node"]["studios"]["edges"] if st["isMain"] == True]
                    i["node"]["studios"]["edges"] = studios
                    data.append(i)
                    name_ = i["node"]["title"]["romaji"]
            
                
        return data

    def response_handle(self):
        data = self.anilist_query(self.name)
        if data["data"]["Page"]["media"] == []:
            name_ = self.name.replace("(", "").replace(")", "")
            data = self.anilist_query(name_)
            if data["data"]["Page"]["media"] == []:
                name_ = self.name.split("(")
                data = self.anilist_query(name_[0])
                
        resp = data["data"]["Page"]["media"]
        
        if resp != []:          
            studios = [st for st in resp[0]["studios"]["edges"] if st["isMain"] == True]
            rel = self.get_sequel(self.name)
            resp[0]["relations"]["edges"] = rel
            resp[0]["studios"]["edges"] = studios
            return resp
            
        else:
            return []
    
