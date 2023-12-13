import requests
import pandas as pd
import time


class ApiFetch:
    """
    Classe responsável por buscar dados da API da Riot Games.
    """

    URL = "https://br1.api.riotgames.com"
    URL2 = "https://americas.api.riotgames.com"

    KEY = "RGAPI-3e66e9c4-be2b-4e7f-86c9-7374743341b0"

    def __init__(self, summoners_name) -> None:
        """
        Inicializa a classe ApiFetch.

        Args:
            summoners_name (str): O nome do invocador.
        """
        self.summoners_name = summoners_name
        self.apiKey = self.KEY
        self.summoner_id = self.fetch_summoner_puuid()
        self.champion_data = self.fetch_champion_data()
    
    def fetch_summoner_puuid(self) -> str:
        """
        Busca o PUUID do invocador.

        Returns:
            str: O PUUID do invocador.
        """
        url = f"{self.URL}/lol/summoner/v4/summoners/by-name/{self.summoners_name}?api_key={self.apiKey}"
        response = requests.get(url)
        response = response.json()
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
        data = response.json()

        print(data)

        participant_data = next((participant for participant in data['info']['participants'] if participant['puuid'] == self.summoner_id), None)

        kills = participant_data['kills']
        deaths = participant_data['deaths']
        assists = participant_data['assists']
        
        if deaths == 0:
            kda = 'Perfect'
        else:
            kda = round((kills + assists) / deaths, 2)

        champion_id = participant_data['championId']
        champion_data = self.fetch_champion_data()
        champion_name = champion_data[str(champion_id)]


        return {'match_data': data, 'kills': kills, 'deaths': deaths, 'assists': assists, 'kda': kda, 'champion_name': champion_name, 'champion_id':champion_id}

    
    def fetch_summoner_data(self) -> dict:
        url = f'{self.URL}/lol/summoner/v4/summoners/by-name/{self.summoners_name}?api_key={self.apiKey}'
        print(url)
        response = requests.get(url)
        print(response.json())
        return response.json()
    
    def fetch_all_match_data(self, match_ids):
        """
        Busca os dados de todas as partidas da lista.

        Args:
            match_ids (list): Lista contendo os IDs das partidas. 

        Returns:
            list: Uma lista de dicionarios, onde cada dicionario contem os dados da partida.
        """

        all_match_data = []
        wins = 0

        for match_id in match_ids:
            match_data = self.fetch_match_data(match_id)
            all_match_data.append(match_data)

            for participant in match_data['info']['participants']:
                if participant['puuid'] == self.summoner_id:
                    if participant['win']:
                        wins += 1
                    break
        print(match_data)
        win_rate = wins / len(match_ids) * 100 if match_ids else 0
        

        return {'match_data': all_match_data, 'win_rate': win_rate}
    
    def fetch_champion_mastery_data(self):
        url = f'{self.URL}/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.summoner_id}?api_key={self.apiKey}'
        response = requests.get(url)
        return response.json()
    
    def fetch_champion_data(self):
        url = f'https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json'
        response = requests.get(url)
        data = response.json()

        champion_data = {champ['key']: champ['name'] for champ in data['data'].values()}

        return champion_data

class Match(ApiFetch):
    """
    Classe que representa uma partida.
    """

    def __init__(self, match_id) -> None:
        """
        Inicializa a classe Match.

        Args:
            api_fetch (ApiFetch): Uma instância da classe ApiFetch.
            match_id (str): O ID da partida.
        """
        self.match_id = match_id
        self.match_data = self.fetch_match_data()
        self.match_duration = self.match_data['info']['gameDuration']
        self.game_mode = self.match_data['info']['gameMode']
        self.game_version = self.match_data['info']['gameVersion']
        self.participants = self.match_data['info']['participants']

    def get_details(self) -> dict:
        return {
            'match_id': self.match_id,
            'match_duration': self.match_duration,
            'game_mode': self.game_mode,
            'game_version': self.game_version
        }

    def fetch_match_data(self) -> dict:
        url = f'{self.URL2}/lol/match/v5/matches/{self.match_id}?api_key={self.KEY}'
        response = requests.get(url)
        data = response.json()

        return data

    def fetch_champion_icon(self) -> None:
        """
        Busca o ícone do campeão do participante.
        """
        version = '13.24.1'
        url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{self.champion_name}.png'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'static/images/{self.champion_name}.png', 'wb') as f:
                f.write(response.content)
        else:
            print(f'Erro ao buscar o ícone para {self.champion_name}: {response.status_code}')

    def fetch_all_champion_icons(self) -> None:
        for participant in self.participants:
            self.champion_name = participant['championName']
            self.fetch_champion_icon()


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
        self.win = participant_data['win']
    
    def fetch_champion_icon(self) -> None:
        """
        Busca o ícone do campeão do participante.
        """
        version = '13.24.1'
        url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{self.champion_name}.png'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'static/images/{self.champion_name}.png', 'wb') as f:
                f.write(response.content)
        else:
            print(f'Erro ao buscar o ícone para {self.champion_name}: {response.status_code}')

    def fetch_all_champion_icons(self) -> None:
        for participant in self.participants:
            self.champion_name = participant['championName']
            self.fetch_champion_icon()
    
    def get_details(self) -> dict:
        participant_data = self.participants[self.participant_id]
        return {
            'summoner_nick': participant_data['summonerName'],
            'champion_name': participant_data['championName'],
            'kills': participant_data['kills'],
            'deaths': participant_data['deaths'],
            'assists': participant_data['assists']
        }

class Summoner(ApiFetch):

    def __init__(self, summoners_name) -> None:
        super().__init__(summoners_name)
        self.summoner_response = self.fetch_summoner_puuid() 
        self.name = self.summoner_response['name']
        self.summoner_lvl = self.summoner_response['summonerLevel']
        self.summoner_id = self.summoner_response['id']
        self.summoner_icon = self.summoner_response['profileIconId']
        self.summoner_rank, self.summoner_tier = self.fetch_rank() 
    
    def fetch_summoner_puuid(self) -> str:
        url = f"{self.URL}/lol/summoner/v4/summoners/by-name/{self.summoners_name}?api_key={self.apiKey}"
        response = requests.get(url)
        response = response.json()

        return response
    
    def fetch_rank(self):
        url = f"{self.URL}/lol/league/v4/entries/by-summoner/{self.summoner_id}?api_key={self.apiKey}"
        response = requests.get(url)
        response = response.json()
        print(response)
        
        if response:
            return response[0]['tier'], response[0]['rank']
        else:
            return None, None

    def fetch_league_id(self):
        summoner_id = self.summoner_response['id']
        url = f"{self.URL}/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={self.apiKey}"
        response = requests.get(url)
        response = response.json()

        if response:
           return response[0]['leagueId']
        else:
           return None 