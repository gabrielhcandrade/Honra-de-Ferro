import json
from typing import List, Dict, Union
from jogador_ranking import JogadorRanking 

class RankingManager:
    def __init__(self, nome_arquivo: str = "../assets/ranking/ranking_data.json") -> None: 
        self._nome_arquivo = nome_arquivo
        self._jogadores: List[JogadorRanking] = []
        self.carregar_de_arquivo()

    def get_jogadores(self) -> List[JogadorRanking]:
        return self._jogadores

    def carregar_de_arquivo(self) -> None:
        try:
            with open(self._nome_arquivo, 'r') as f:
                dados: List[Dict[str, Union[str, int]]] = json.load(f)
                self._jogadores = [JogadorRanking(j['nome'], j['pontuacao']) for j in dados]
        except (IOError, json.JSONDecodeError):
            self._jogadores = []
            print(f"Aviso: Arquivo de ranking '{self._nome_arquivo}' não encontrado ou inválido. Criando novo.")

    def adicionar_jogador(self, jogador: JogadorRanking) -> None:
        if not self.existe_nome(jogador.get_nome()):
            self._jogadores.append(jogador)
            self._jogadores.sort(key=lambda x: x.get_pontuacao(), reverse=True)
            self.salvar_em_arquivo()

    def salvar_em_arquivo(self) -> None:
        try:
            with open(self._nome_arquivo, 'w') as f:
                json.dump([j.to_dict() for j in self._jogadores], f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar ranking: {e}")

    def existe_nome(self, nome: str) -> bool:
        return any(j.get_nome().lower() == nome.lower() for j in self._jogadores)