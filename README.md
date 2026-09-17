# The Farmer Was Replaced — minha jornada em Python

Código da minha fazenda automatizada no jogo **The Farmer Was Replaced**, onde se programa um drone em Python para plantar, colher e resolver desafios. Este repositório é o registro da minha jornada de aprendizado: tentativa, erro e evolução até chegar em soluções eficientes e paralelas.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `main.py` | Loop principal (roda a estratégia atual) |
| `Utilidades.py` | Base: `move_to`, `andar`, `for_all` (paralelização multi-drone), rega |
| `FAZENDA.py` | `plantar_e_colher(tipo)` — colhe e replanta cada casa **na mesma passada**, em paralelo |
| `GRAMA.py` / `MADERA.py` / `CENOURA.py` | Culturas simples paralelizadas |
| `ABOBORA.py` | Abóbora com fusão em bloco gigante (rende `n×n×6`) |
| `CACTO.py` | Cacto: planta, **ordena o campo** (linhas e colunas) e colhe tudo de uma vez |
| `POLICULTURA.py` | Policultura paralela: planta cultura + acompanhante (`get_companion`) para bônus de rendimento |
| `MAZE.py` | Labirinto — seguidor de parede (mão esquerda) |
| `segundoMAZE.py` | Labirinto — **DFS guiada por `measure()`** (mais eficiente) |
| `DINOSSAURO.py` | "Cobrinha" com chapéu de dinossauro — ciclo hamiltoniano para colher ossos |
| `DINHEIRO.py` | Runner que farma ouro resolvendo labirintos |

## Destaques técnicos

### Multi-drone (paralelização)
`Utilidades.for_all(f)` roda uma função em cada casa usando **todos os drones disponíveis** (um por linha), no padrão `if not spawn_drone(tarefa): tarefa()`, esperando todos terminarem. Cada drone trabalha em casas disjuntas para evitar condição de corrida.

### Labirinto
- **Seguidor de parede** (`MAZE.py`): simples (~10 linhas). Em labirinto sem loops, colar numa parede leva a todos os corredores.
- **DFS guiada** (`segundoMAZE.py`): usa `measure()` para pegar a posição do tesouro e anda na direção dele com backtracking. Gasta bem menos movimentos (que custam 200 ticks), enquanto `can_move()` custa ~1.

### Cacto
A colheita só se espalha com o campo **ordenado** (linhas crescentes O→L, colunas S→N). Como só dá para trocar vizinhos (`swap`), uso **bubble sort** por linha e por coluna, paralelizado (um drone por linha/coluna).

### Abóbora
Fundem num bloco gigante quando **todas** estão crescidas (`n×n×6`). Como 20% morrem ao crescer, o código replanta em paralelo até o campo fundir.

### Dinossauro (cobrinha)
Come maçãs (compradas com cacto) para crescer a cauda; ao trocar de chapéu recebe `comprimento²` ossos. A versão final usa um **ciclo hamiltoniano** que cobre o campo inteiro sem a cobra se morder, com `set_world_size` garantindo campo par.

## Desafios e aprendizados (a parte de tentativa e erro)

- **Labirinto — do simples ao eficiente:** comecei com o seguidor de parede (funciona, mas varre o campo todo por um tesouro). Pesquisei e migrei para **DFS guiada por `measure()`**, que é o que a comunidade considera mais eficiente para um único tesouro. Aprendi que o BFS "ótimo" não ajuda aqui, porque mapear o labirinto exige andar por ele do mesmo jeito.

- **Cacto — nem todo algoritmo serve:** como só se troca vizinhos, tive que usar **bubble sort** (não dá para counting sort). A dica do jogo salvou: "com as linhas ordenadas, ordenar as colunas não as desordena".

- **Dinossauro — a saga da cobrinha:** essa foi a mais difícil.
  - Ciclo hamiltoniano puro: **seguro mas lento**.
  - Guloso com `measure()`: **rápido mas encurralava**.
  - Híbrido (ciclo + atalhos): rodava no canto → depois no meio → depois num loop. Descobri que os bugs eram (1) o limite do atalho errado (usava `N - len` em vez da distância real até a cauda), (2) faltava margem de segurança (regra de Tapsell: `distância_cauda - tamanho - folga`), e (3) o método `.discard()` de `set` **não existe** no Python do jogo (troquei por `.remove()`).
  - No fim, escolhi a **versão segura** (ciclo hamiltoniano puro): confiável e garantida.

- **Paridade importa:** o ciclo hamiltoniano só fecha em **campo de tamanho par**. Resolvi usando `set_world_size` para forçar par automaticamente.

- **Policultura e paralelização:** o acompanhante cai numa casa vizinha (até 3), então drones de linhas vizinhas podem brigar pela mesma casa. Paralelizei mesmo assim usando **posição absoluta (`move_to`)** por linha, aceitando pequenas perdas de bônus nas bordas em troca de muito mais velocidade.

- **A pegadinha da ferramenta:** com o jogo aberto, ele **regrava/apaga** os arquivos no disco a cada autosave. Aprendi a editar dentro do editor do jogo ou fechar o jogo antes de salvar de fora.

- **Escalar com drones:** o `for_all` usa até `max_drones()` (um por linha). Enquanto o número de drones for ≤ número de linhas, ele aproveita todos automaticamente, sem mudar o código.
