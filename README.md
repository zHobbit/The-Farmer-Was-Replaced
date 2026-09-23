# The Farmer Was Replaced — minha jornada em Python

Código da minha fazenda automatizada no jogo **The Farmer Was Replaced**, onde se programa um drone em Python para plantar, colher e resolver desafios. Este repositório é o registro da minha jornada de aprendizado: tentativa, erro, medição e evolução até chegar em soluções eficientes e paralelas.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `main.py` | Loop principal (roda a estratégia atual) |
| `Utilidades.py` | Base: `move_to`, `for_all` (paralelização multi-drone), fertilizante com histerese e troca de chapéu |
| `FAZENDA.py` | `plantar_e_colher(tipo)` — planta, fertiliza, colhe e replanta cada casa **na mesma passada**, em paralelo |
| `GRAMA.py` / `MADERA.py` / `CENOURA.py` | Culturas simples paralelizadas |
| `ABOBORA.py` | Abóbora com fusão em bloco gigante (rende `n×n×6`) |
| `CACTO.py` | Cacto: planta, **ordena o campo** (linhas e colunas) e colhe tudo de uma vez |
| `POLICULTURA.py` | Policultura paralela **em 3 fases**: cultura + acompanhante (`get_companion`) sem disputa entre drones |
| `MAZE.py` | Labirinto — seguidor de parede (mão esquerda) |
| `segundoMAZE.py` | Labirinto — DFS guiada por `measure()` |
| `mapaMAZE.py` | Labirinto — **mapa + reaproveitamento do labirinto** (o mais rápido) |
| `MEDIR.py` | Corrida entre os algoritmos de labirinto, medida com `get_tick_count()` |
| `DINOSSAURO.py` | "Cobrinha" com chapéu de dinossauro — ciclo hamiltoniano para colher ossos |
| `DINHEIRO.py` | Runner que farma ouro com o `mapaMAZE` |

## Destaques técnicos

### Multi-drone (paralelização)
`Utilidades.for_all(f)` roda uma função em cada casa usando **todos os drones disponíveis** (um por linha), no padrão `if not spawn_drone(tarefa): tarefa()`, esperando todos terminarem. Cada drone trabalha em casas disjuntas para evitar condição de corrida.

### Labirinto com mapa (`mapaMAZE.py`)
Usar `Weird_Substance` **em cima do tesouro** coleta o ouro e sorteia um tesouro novo **no mesmo labirinto** (até 300 vezes). Então o drone anota numa tabela os vizinhos alcançáveis de cada casa enquanto anda:
- **1º tesouro:** explora com DFS guiada por `measure()` e vai mapeando.
- **Próximos:** **BFS no mapa** dá o caminho mais curto por casas conhecidas, sem explorar. Se o tesouro caiu numa parte não mapeada, vai até a casa conhecida mais perto e explora dali.
- Paredes só **somem** entre um tesouro e outro, então uma passagem anotada como aberta continua aberta.
- Um mapa novo para cada labirinto.

### Medindo com o timer (`MEDIR.py`)
`get_tick_count()` conta os ticks de execução, o custo do jogo, que não muda com velocidade ou energia. Medir é grátis. Resultado de 30 tesouros num campo 32×32:

| Versão | ticks/tesouro | tempo real |
|---|---|---|
| `segundoMAZE` (labirinto novo a cada tesouro) | 201.874 | ~33 min |
| `mapaMAZE` (primeira versão) | 103.299 | ~17 min |
| `mapaMAZE` otimizado | **58.977** | **~10 min** |

**3,4× mais rápido** que o `segundoMAZE`, com o mesmo ouro e a mesma substância gasta.

### Fertilizante com histerese
Cada casa é fertilizada até a planta ficar pronta. Quando o estoque **zera**, para; só volta a fertilizar quando juntar **50.000** de novo. Planta fertilizada fica infectada e metade da colheita vira `Weird_Substance`, que alimenta os labirintos. O cacto fica de fora de propósito: cresce em ~1s, e a infecção cortaria pela metade a colheita do campo ordenado.

### Um chapéu por função
Cada função equipa o seu (`Straw`, `Tree`, `Carrot`, `Pumpkin`, `Cactus`, `Green`, `Brown`, `Wizard`, `Gold`, `Dinosaur`), para saber de longe o que está rodando. Trocar de chapéu no começo dos labirintos também tira o de dinossauro, que impedia o labirinto de crescer.

### Cacto
A colheita só se espalha com o campo **ordenado** (linhas crescentes O→L, colunas S→N). Como só dá para trocar vizinhos (`swap`), uso **bubble sort** por linha e por coluna, paralelizado.

### Abóbora
Fundem num bloco gigante quando **todas** estão crescidas (`n×n×6`). Como 20% morrem ao crescer, o código replanta em paralelo até o campo fundir.

### Dinossauro (cobrinha)
Come maçãs (compradas com cacto) para crescer a cauda; ao trocar de chapéu recebe `comprimento²` ossos. A versão final usa um **ciclo hamiltoniano** que cobre o campo inteiro sem a cobra se morder, com `set_world_size` garantindo campo par.

## Desafios e aprendizados (a parte de tentativa e erro)

- **Labirinto — três gerações:** seguidor de parede (simples, mas varre tudo) → DFS guiada por `measure()` → **mapa + reaproveitamento**. Pra um labirinto de um tesouro só, mapear não ajuda, porque é preciso andar pra descobrir o mapa. A virada foi perceber que o **mesmo labirinto pode render até 300 tesouros**, e aí o mapa passa a valer muito.

- **Medir antes de otimizar:** a primeira medição mostrou a curva do mapa **ao contrário**: o 1º tesouro custou 45 mil ticks, e os seguintes, 105 mil. A doc de tempo explicou: **cada operação de código também custa tick**, e conjunto/dicionário cobram pelo tamanho da chave. O BFS recalculava o mapa inteiro a cada tesouro. As correções: parar o BFS ao achar o tesouro, casas como número (`y * tamanho + x`) em vez de tupla, o mapa guardando os vizinhos prontos e o tamanho do campo lido uma vez só. Depois disso os tesouros seguintes caíram pra ~52 mil ticks, **4,5× mais baratos que o primeiro**.

- **O `move_to` que dava a volta no mundo:** pra ir 2 casas pro Oeste, a distância é −2, e −2 é sempre menor que `tamanho/2`, então ele ia pro Leste e dava a volta no campo inteiro. Quase não aparecia na fazenda, mas na policultura (pulos curtos pra trás o tempo todo) pesava muito. Hoje ele vai pelo caminho mais curto e anda um número fixo de passos, então nunca fica preso num `while`.

- **Policultura — três versões até ficar sem disputa:** 1 drone por linha dava avisos *"Não é possível plantar Carrot em Grassland"*: o `till()` **alterna** o chão, e dois drones arando a mesma casa se anulavam. Rodar em **ondas** de linhas a 7 de distância resolveu, mas usava poucos drones. A versão final tem **3 fases** (plantar e anotar pedidos → plantar acompanhantes → colher), e em cada fase cada drone só mexe na própria linha. Os drones devolvem os pedidos pelo `wait_for`.

- **Cacto — nem todo algoritmo serve:** como só se troca vizinhos, tive que usar **bubble sort**. A dica do jogo salvou: "com as linhas ordenadas, ordenar as colunas não as desordena".

- **Dinossauro — a saga da cobrinha:** ciclo puro (**seguro mas lento**) → guloso com `measure()` (**rápido mas encurralava**) → híbrido com atalhos (rodava no canto, no meio, em loop). Os bugs: limite de atalho errado, falta da margem de Tapsell e o `.discard()` de `set`, que **não existe** no Python do jogo. No fim, fiquei com a versão segura. E o ciclo hamiltoniano só fecha em **campo par**, resolvido com `set_world_size`.

- **A pegadinha da ferramenta:** com o jogo aberto, ele **regrava/apaga** os arquivos no disco a cada autosave. Aprendi a editar dentro do editor do jogo ou fechar o jogo antes de salvar de fora.

- **Escalar com drones:** o `for_all` usa até `max_drones()` (um por linha). Enquanto o número de drones for ≤ número de linhas, ele aproveita todos automaticamente.
