# The Farmer Was Replaced — minha jornada em Python

Código da minha fazenda automatizada no jogo **The Farmer Was Replaced**, onde se programa um drone em Python pra plantar, colher e resolver desafios.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `main.py` | Loop principal: faz o rodízio das culturas por prioridade |
| `Utilidades.py` | Funções base: `move_to`, `andar`, `for_all` (paralelização com drones), rega, etc. |
| `FAZENDA.py` | `plantar_e_colher(tipo)` — colhe e replanta cada casa **na mesma passada**, em paralelo |
| `GRAMA.py` / `MADERA.py` / `CENOURA.py` | Culturas simples (feno, madeira, cenoura) paralelizadas |
| `ABOBORA.py` | Abóbora com fusão em bloco gigante (rende `n×n×6`) |
| `CACTO.py` | Cacto: planta, **ordena o campo** (linhas e colunas) e colhe tudo de uma vez |
| `MAZE.py` | Labirinto — seguidor de parede (regra da mão esquerda) |
| `segundoMAZE.py` | Labirinto — **DFS guiada por `measure()`** (mais eficiente que o seguidor de parede) |
| `TESTE.py` | Runner de testes |

## Destaques técnicos

### Multi-drone (paralelização)
`Utilidades.for_all(f)` roda uma função em cada casa da fazenda usando **todos os drones disponíveis** (um por linha), no padrão oficial `if not spawn_drone(tarefa): tarefa()`, e espera todos terminarem. Cada drone trabalha em casas disjuntas, evitando condição de corrida.

### Labirinto
Duas soluções:
- **Seguidor de parede** (`MAZE.py`): simples (~10 linhas). Num labirinto sem loops, colar numa parede leva a todos os corredores.
- **DFS guiada** (`segundoMAZE.py`): usa `measure()` pra pegar a posição do tesouro e anda sempre na direção dele, com backtracking. Gasta bem menos movimentos (que custam 200 ticks cada), enquanto sondar com `can_move()` é quase de graça.

### Cacto
A colheita se espalha só quando o campo está **ordenado** (linhas crescentes Oeste→Leste, colunas Sul→Norte). Como só dá pra trocar vizinhos (`swap`), uso **bubble sort** por linha e por coluna — paralelizando com um drone por linha/coluna.

### Abóbora
Abóboras fundem num bloco gigante quando **todas** estão crescidas (rende `n×n×6`). Como 20% morrem ao crescer, o código replanta em paralelo até o campo inteiro fundir, aí colhe.
