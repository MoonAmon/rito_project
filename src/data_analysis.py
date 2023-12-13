from src.data_collection import Match
import pandas as pd

class Analytics:
    def __init__(self, api_fetch, match_id) -> None:
        """
        Inicializa uma instância da classe Analytics.

        Args:
            api_fetch (APIFetch): Uma instância da classe APIFetch.
            match_id (int): O ID da partida.

        Returns:
            None
        """
        super().__init__(api_fetch, match_id)
        self.match_df = self.get_dataframe_match()

    def get_dataframe_match(self):
        """
        Recupera os dados da partida e retorna-os como um DataFrame do pandas.

        Returns:
            pd.DataFrame: Um DataFrame contendo os dados da partida.
        """
        participants_df = pd.DataFrame()

        for participant in self.participants:
            participant_info = {
                'championName': participant['championName'],
                'kills': participant['kills'],
                'death': participant['deaths'],
                'assists': participant['assists'],
                'totalDamageToChampions': participant['totalDamageDealtToChampions'],
                'goldEarned': participant['goldEarned'],
                'visioScore': participant['visionScore'],
                'role': participant['individualPosition'],
                'teamId': participant['teamId']
            }
            participants_df = pd.concat([participants_df, pd.DataFrame([participant_info])], ignore_index=True)

        return participants_df

