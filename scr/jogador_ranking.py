from typing import Dict, Union


class JogadorRanking:
    def __init__(self, nome: str, pontuacao: int) -> None:
        self.nome = nome
        self.pontuacao = pontuacao

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {"nome": self.nome, "pontuacao": self.pontuacao}

    @staticmethod
    def from_dict(data: Dict[str, Union[str, int]]) -> 'JogadorRanking':
        return JogadorRanking(data["nome"], data["pontuacao"])

    def __repr__(self) -> str:
        return f"{self.nome}: {self.pontuacao} pts"