import requests
import pandas as pd
import time

class ApiFetch:
    """
    Classe responsável por buscar dados da API da Riot Games.
    """

    URL = "https://br1.api.riotgames.com"
    URL2 = "https://americas.api.riotgames.com"

    KEY = "RGAPI-5e7ba6ad-ff48-435b-a8b7-b3a3b71ee2cb"

    def __init__(self, summoners_name) -> None:
        """
        Inicializa a classe ApiFetch.

        Args:
            summoners_name (str): O nome do invocador.
        """
        self.summoners_name = summoners_name
        self.apiKey = self.KEY
        self.summoner_id = self.fetch_summoner_puuid()
    
    def fetch_summoner_puuid(self) -> str:
        """
        Busca o PUUID do invocador.

        Returns:
            str: O PUUID do invocador.
        """
        url = f"{self.URL}/lol/summoner/v4/summoners/by-name/{self.summoners_name}?api_key={self.apiKey}"
        response = requests.get(url)
        response = response.json()
        time.sleep(1)
        return response["puuid"]

    def fetch_match_id(self, count=10) -> list:
        """
        Busca os IDs das partidas do invocador.

        Args:
            count (int, optional): O número de IDs de partida a serem buscados. O padrão é 10.

        Returns:
            list: Uma lista de IDs de partida.
        """
        url = f'{self.URL2}/lol/match/v5/matches/by-puuid/{self.summoner_id}/ids?start={0}&count={count}&api_key={self.apiKey}'
        print(url)
        response = requests.get(url)
        time.sleep(1)
        return response.json()

    def fetch_match_data(self, match_id) -> dict:
        """
        Busca os dados de uma partida específica.

        Args:
            match_id (str): O ID da partida.

        Returns:
            dict: Um dicionário contendo os dados da partida.
        """
        url = f'{self.URL2}/lol/match/v5/matches/{match_id}?api_key={self.apiKey}'
        response = requests.get(url)
        time.sleep(1)
        return response.json()
    
   

class Match:
    """
    Classe que representa uma partida.
    """

    def __init__(self, api_fetch, match_id) -> None:
        """
        Inicializa a classe Match.

        Args:
            api_fetch (ApiFetch): Uma instância da classe ApiFetch.
            match_id (str): O ID da partida.
        """
        self.match_id = match_id
        self.match_data = api_fetch.fetch_match_data(match_id)
        self.match_duration = self.match_data['info']['gameDuration']
        self.game_mode = self.match_data['info']['gameMode']
        self.game_version = self.match_data['info']['gameVersion']
        self.participants = self.match_data['info']['participants']



class Participants(Match):
    """
    Classe que representa um participante de uma partida.
    """

    def __init__(self, api_fetch, match_id, participant_id) -> None:
        """
        Inicializa a classe Participants.

        Args:
            api_fetch (ApiFetch): Uma instância da classe ApiFetch.
            match_id (str): O ID da partida.
            participant_id (int): O ID do participante.
        """
        super().__init__(api_fetch, match_id)
        participant_data = self.participants[participant_id]
        self.summoner_name = participant_data['summonerName']
        self.kills = participant_data['kills']
        self.deaths = participant_data['deaths']
        self.assists = participant_data['assists']
        self.vision_score = participant_data['visionScore'] 
        self.champion_name = participant_data['championName']
        self.lane = participant_data['lane'] 
        self.level = participant_data['champLevel']
        self.totalDamage = participant_data['totalDamageDealt']
    
    def fetch_champion_icon(self):
        """
        Busca o ícone do campeão do participante.
        """
        version = '11.8.1'
        url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{self.champion_name}.png'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'static/images/{self.champion_name}.png', 'wb') as f:
                f.write(response.content)
        else:
            print(f'Erro ao buscar o ícone para {self.champion_name}: {response.status_code}')

    def fetch_all_champion_icons(self):
        for participant in self.participants:
            self.champion_name = participant['championName']
            self.fetch_champion_icon()