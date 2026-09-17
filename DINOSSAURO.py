import Utilidades

# ============================================================================
# Dinossauro (snake) VERSAO SEGURA: segue um CICLO HAMILTONIANO puro que passa
# por TODAS as casas e volta ao inicio. A cobra cresce sem nunca se morder, ate
# encher o campo. Simples e garantido (sem atalhos, sem loops).
#
# set_world_size deixa o campo PAR (o ciclo so fecha em par), limpa a fazenda e
# volta ao tamanho normal quando a execucao acaba. Precisa de CACTOS (as macas
# sao compradas com cacto).
# ============================================================================

def rota():
	# direcoes de um ciclo hamiltoniano (N movimentos, volta ao ponto inicial):
	# sobe a coluna 0, serpenteia as colunas 1..size-1 pelas linhas 1..size-1,
	# desce e volta pela linha 0.
	size = get_world_size()
	dirs = []
	for i in range(size - 1):
		dirs.append(North)
	for x in range(1, size):
		dirs.append(East)
		for i in range(size - 2):
			if x % 2 == 1:
				dirs.append(South)
			else:
				dirs.append(North)
	dirs.append(South)
	for i in range(size - 1):
		dirs.append(West)
	return dirs


def Dinossauro():
	if num_items(Items.Cactus) <= 0:
		return                            # sem cacto nao nasce maca

	# campo PAR (limpa a fazenda e volta ao normal no fim da execucao)
	alvo = get_world_size()
	if alvo % 2 == 1:
		alvo = alvo - 1
	if alvo < 4:
		alvo = 4
	set_world_size(alvo)
	Utilidades.move_to(0, 0)

	change_hat(Hats.Dinosaur_Hat)         # equipa -> nasce uma maca sob o drone

	caminho = rota()
	cheio = False
	cactos_antes = num_items(Items.Cactus)
	while not cheio:
		for d in caminho:
			if not move(d):              # bateu na propria cauda = campo cheio
				cheio = True
				break
		agora = num_items(Items.Cactus)
		if agora == cactos_antes:        # nenhuma maca comprada nessa volta -> parou de crescer
			cheio = True
		cactos_antes = agora

	change_hat(Hats.Straw_Hat)            # troca o chapeu -> colhe a cauda (comprimento**2 ossos)
