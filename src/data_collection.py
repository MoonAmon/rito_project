import requests
import time

class ApiFetch:
    URL = "https://br1.api.riotgames.com"
    URL2 = "https://americas.api.riotgames.com"

    KEY = "RGAPI-5e7ba6ad-ff48-435b-a8b7-b3a3b71ee2cb"

    def __init__(self, summoners_name, summoner_id=None) -> None:
        self.summoners_name = summoners_name
        self.apiKey = self.KEY
        self.summoner_id = self.fetch_summoner_puuid()
    
    def fetch_summoner_puuid(self):
        url = f"{self.URL}/lol/summoner/v4/summoners/by-name/{self.summoners_name}?api_key={self.apiKey}"
        response = requests.get(url)
        response = response.json()
        print(response["puuid"])
        time.sleep(1)
        return response["puuid"]

    def fetch_match_id(self, count=10) -> list:
        url = f'{self.URL2}/lol/match/v5/matches/by-puuid/{self.summoner_id}/ids?start={0}&count={count}&api_key={self.apiKey}'
        print(url)
        response = requests.get(url)
        print(response.json())
        time.sleep(1)
        return response.json()

    def fetch_match_data(self, match_id):
        url = f'{self.URL2}/lol/match/v5/matches/{match_id}?api_key={self.apiKey}'
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
    
    
