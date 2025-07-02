from typing import Dict, Union

class JogadorRanking:
    def __init__(self, nome: str, pontuacao: int) -> None:
        self._nome = nome
        self._pontuacao = pontuacao

    def get_nome(self) -> str:
        return self._nome

    def get_pontuacao(self) -> int:
        return self._pontuacao

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {"nome": self._nome, "pontuacao": self._pontuacao}

    @staticmethod
    def from_dict(data: Dict[str, Union[str, int]]) -> 'JogadorRanking':
        return JogadorRanking(data["nome"], data["pontuacao"])

    def __repr__(self) -> str:
        return f"{self._nome}: {self._pontuacao} pts"