import requests
import time
import pandas as pd

class ApiFetch:
    URL = "https://americas.api.riotgames.com"

    def __init__(self, apiKey, summonerNick, summonerTag, puuid=None) -> None:
        self.apiKey = apiKey
        self.summoner_nick = summonerNick
        self.summoner_tag = summonerTag
        self.summoner_id = puuid
    
    def fetch_summoner_id(self):
        url = f'{self.URL}/riot/account/v1/accounts/by-riot-id/{self.summoner_nick}/{self.summoner_tag}?api_key={self.apiKey}'
        response = requests.get(url)
        response = response.json()
        print(response)
        time.sleep(1)
        self.summoner_id = response['puuid']


    def fetch_match_id(self, count=10) -> list:
        url = f'{self.URL}/lol/match/v5/matches/by-puuid/{self.summoner_id}/ids?start={0}&count={count}&api_key={self.apiKey}'
        response = requests.get(url)
        time.sleep(1)
        print(url)
        print(response.json())
        return response.json()

    def fetch_match_data(self, match_id):
        url = f'{self.URL}/lol/match/v5/matches/{match_id}?api_key={self.apiKey}'
        response = requests.get(url)
        time.sleep(1)
        return response.json()

class Match:
    def __init__(self, api_fetch, match_id) -> None:
        self.match_id = match_id
        self.match_data = api_fetch.fetch_match_data(match_id)
        self.match_duration = self.match_data['info']['gameDuration']
        self.game_mode = self.match_data['info']['gameMode']
        self.game_version = self.match_data['info']['gameVersion']
        self.participants = self.match_data['info']['participants']



class Participants(Match):
    def __init__(self, api_fetch, match_id, participant_id) -> None:
        super().__init__(api_fetch, match_id)
        participant_data = self.participants[participant_id]
        self.summoner_name = None
        self.kills = None
        self.deaths = None
        self.assists = None
        self.vision_score = None
        self.champion_name = None
        self.role = None
        self.level = None
        self.totalDamage = None
    
    
match = ApiFetch("RGAPI-0a0dfc77-970e-45ad-8ecf-63037fa1b2d6","suzuhatitor", "psyko","")
match.fetch_match_id()
