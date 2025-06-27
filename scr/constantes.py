from typing import Tuple

class Constantes:
    LARGURA: int = 1920
    ALTURA: int = 1080
    ROWS: int = 16
    TILE_SIZE: int = ALTURA // ROWS

    PRETO: tuple[int, int, int]= (0, 0, 0)
    BRANCO: tuple[int, int, int]= (255, 255, 255)
    VERMELHO: tuple[int, int, int]= (255, 0, 0)
    VERDE: tuple[int, int, int]= (0, 255, 0)
    ROSA: tuple[int, int, int]= (0, 127, 255)
    AMARELO: tuple[int, int, int] = (255, 255, 0)


    COR_TEXTO: Tuple[int, int, int] = (255, 255, 255)
    COR_SELECIONADA: Tuple[int, int, int] = (200, 200, 0)
    COR_BOTAO: Tuple[int, int, int] = (100, 100, 100)
    COR_SLIDER: Tuple[int, int, int] = (180, 180, 180)

    GRAVIDADE: float = 1.5
    VEL_MAX_QUEDA: float = 15
    Y_CHAO = 400