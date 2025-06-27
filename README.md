# Honra de Ferro

Honra de Ferro é um jogo de plataforma 2D com elementos de ação e RPG, desenvolvido como um projeto completo para a disciplina de Computação Orientada a Objetos. Enfrente hordas de esqueletos amaldiçoados e um dragão temível para provar seu valor e gravar seu nome no ranking dos maiores guerreiros!

O projeto foi construído com ênfase nos princípios da disciplina de Programação Orientada a Objetos (POO) em Python, resultando em um código limpo, modular e de fácil manutenção, conforme as diretrizes acadêmicas. 

## 🎮 Sobre o Jogo
Em "Honra de Ferro", o jogador assume o papel de um bravo guerreiro que deve sobreviver a ondas de inimigos em um cenário de fantasia sombria. A jornada é dividida em fases, começando com o combate contra esqueletos ágeis e culminando em uma batalha épica contra um chefe dragão que cospe fogo.

- Funcionalidades Implementadas Combate Dinâmico: Ataque com sua espada, bloqueie golpes inimigos e use uma investida (dash) para se esquivar com agilidade.
- Inimigos com IA: Esqueletos perseguem o jogador e atacam quando ele se aproxima. O dragão ataca à distância com bolas de fogo.
- Sistema de Fases: A batalha progride em fases, com a dificuldade aumentando até o confronto final contra o chefe.
- Power-ups: Inimigos derrotados podem dropar poções que curam a vida do jogador ao serem coletadas.
- Menu Completo: Um menu inicial robusto permite iniciar um novo jogo, ver o ranking de pontuações, acessar as configurações e sair do jogo.
- Configurações de Áudio: Ajuste os volumes da música de fundo e dos efeitos sonoros de forma independente.
- Sistema de Ranking Persistente: Sua pontuação final é salva em um arquivo JSON.  Compita para alcançar o topo do ranking!
- Salvar e Continuar: O progresso do jogo é salvo automaticamente ao avançar de fase. Se for derrotado, você pode continuar do último checkpoint. 

## 🛠️ Tecnologias Utilizadas
Linguagem: Python 3
Biblioteca Principal: Pygame - para renderização, manipulação de eventos e áudio.
Arquitetura: Programação Orientada a Objetos (POO), seguindo os padrões de projeto e as convenções de código detalhadas nas especificações do projeto. 

## 🚀 Como Executar
Para rodar o projeto em sua máquina local, siga os passos abaixo.
1. Clone o Repositório:
```
Bash

git clone https://github.com/seu-usuario/honra-de-ferro.git
cd honra-de-ferro
```
2. Instale as Dependências:
O projeto depende da biblioteca pygame. Você pode instalá-la usando pip.
```
Bash

pip install pygame
```
3. Execute o Jogo:
Navegue até o diretório scr/ e execute o script main.py.
```
Bash

cd "jogoFinal - Copia/scr"
python main.py
```
Controles do Jogo
```
Tecla                          Ação

Setas (Esquerda/Direita)       Mover o personagem

Seta (Cima)                    Pular

Barra de Espaço                Atacar

Shift Esquerdo                Investida (Dash)

E                             Defender

H                             Usar Poção de Cura

ESC                           Pausar / Voltar ao Menu
```
🏛️ Estrutura do Projeto
O código-fonte foi organizado de forma a separar as responsabilidades, facilitando a manutenção e a escalabilidade do projeto.
```
.
├── assets/          # Contém todas as imagens, fontes e sons
│   ├── img/
│   ├── sons/
│   └── ranking/     # Arquivos JSON para savegame e ranking
│
└── scr/             # Código-fonte principal do jogo
    ├── componentes/ # Módulos de componentes reutilizáveis (botão, etc.)
    ├── telas/       # Classes para cada tela do jogo (menu, config)
    ├── asset_manager.py
    ├── batalha_dragao.py
    ├── entidade.py  # Classe base para personagens
    ├── jogador.py
    ├── dragao.py
    ├── esqueleto.py
    ├── game.py      # Classe principal que orquestra o jogo
    └── main.py      # Ponto de entrada da aplicação
```

## 📄 Licença
Este projeto é um trabalho acadêmico e não possui uma licença formal para distribuição ou uso comercial.

## 👨‍💻 Autor
[Gabriel Henrique Correa Andrade] - gabrielhcandrade
Projeto desenvolvido para a disciplina de Computação Orientada a Objetos da Universidade Federal de Viçosa (UFV) - Campus Rio Paranaíba, sob a orientação do Prof. Alan Diego Aurélio Carneiro. 
