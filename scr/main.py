import pygame
import os
from game import Game # CORREÇÃO: Importa a classe Game do mesmo diretório

if __name__ == "__main__":
    # Garante que o diretório de trabalho seja o do script
    # Isso faz com que os caminhos relativos (ex: 'assets/img/fundo.png') funcionem
    script_dir: str = os.path.dirname(__file__)
    if script_dir:
        os.chdir(script_dir)

    # Verificações de diretórios de assets
    if not os.path.exists('../assets/img/guerreiro'): # CORREÇÃO: Caminho relativo para a pasta assets
        print("AVISO: Diretório '../assets/img/guerreiro' não encontrado.")
    if not os.path.exists('../assets/img/inimigo'): # CORREÇÃO: Caminho relativo para a pasta assets
        print("AVISO: Diretório '../assets/img/inimigo' não encontrado.")

    pygame.init()
    jogo: Game = Game()
    jogo.executar()