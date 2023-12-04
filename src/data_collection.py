import requests
import time

class Summoner:
    def __init__(self, summonerNick, summonerTag) -> None:
        self.summonerNick = summonerNick
        self.summonerTag = summonerTag
    
    def set_summoner_id(self):
        pass

class ApiFetch:

    URL = "https://americas.api.riotgames.com"

    def __init__(self, apiKey, summoner_id) -> None:
        self.apiKey = apiKey
        self.summoner_id = summoner_id
    
    def fetch_match_id(self, count=10) -> list:
        url = f'{self.URL}/lol/match/v5/matches/by-puuid/{self.summoner_id}/ids?start={0}&count={count}&api_key={self.apiKey}'
        response = requests.get(url)
        time.sleep(1)
        return response.json()

    def fetch_match_data(self):
        pass

