import pygame
import os
from game import Game 

if __name__ == "__main__":
    script_dir: str = os.path.dirname(__file__)
    if script_dir:
        os.chdir(script_dir)

    if not os.path.exists('../assets/img/guerreiro'): 
        print("AVISO: Diretório '../assets/img/guerreiro' não encontrado.")
    if not os.path.exists('../assets/img/inimigo'): 
        print("AVISO: Diretório '../assets/img/inimigo' não encontrado.")

    pygame.init()
    jogo: Game = Game()
    jogo.executar()