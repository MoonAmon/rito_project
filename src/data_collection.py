import requests
import time

class ApiFetch:
    URL = "https://americas.api.riotgames.com"

    def __init__(self, apiKey, summonerNick, summonerTag) -> None:
        self.apiKey = apiKey
        self.summoner_nick = summonerNick
        self.summoner_tag = summonerTag
        self.summoner_id = self.fetch_summoner_id()
    
    def fetch_summoner_id(self):
        url = f'{self.URL}/riot/account/v1/accounts/by-riot-id/{self.summoner_nick}/{self.summoner_tag}&api_key={self.apiKey}'
        response = requests.get(url)
        time.sleep(1)
        self.summmoner_id = response


    def fetch_match_id(self, count=10) -> list:
        url = f'{self.URL}/lol/match/v5/matches/by-puuid/{self.summoner_id}/ids?start={0}&count={count}&api_key={self.apiKey}'
        response = requests.get(url)
        time.sleep(1)
        return response.json()

    def fetch_match_data(self):
        pass

class Match(ApiFetch):
    def __init__(self, match_id, match_data) -> None:
        self.match_id = match_id
        self.match_duration = match_data['info']['gameDuration']
        self.game_mode = match_data['info']['gameMode']
        self.game_version = match_data['info']['gameVersion']
        self.participants = match_data['info']['participants']

class Participants(Match):
    def __init__(self) -> None:
        self.summoner_nick = None
        self.kills = None
        self.deaths = None
        self.assists = None
        self.vision_score = None
        self.champion_name = None
        self.role = None
        self.level = None
        self.totalDamage = None
    
    
    