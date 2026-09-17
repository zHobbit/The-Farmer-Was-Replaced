import Utilidades

def Maze():
	# limpa o tile. se ja havia um labirinto, dar harvest fora do tesouro faz ele sumir
	harvest()
	# arbusto so cresce em grama; garante o chao certo
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)

	# cresce o labirinto NA HORA no arbusto recem-plantado (nao precisa esperar crescer)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

	# resolve
	resolver_labirinto()


def vira_esquerda(d):
	if d == North:
		return West
	if d == West:
		return South
	if d == South:
		return East
	return North              # d == East


def vira_direita(d):
	if d == North:
		return East
	if d == East:
		return South
	if d == South:
		return West
	return North              # d == West


def resolver_labirinto():
	# seguidor de parede (regra da mao esquerda): num labirinto sem loops todas as
	# paredes sao uma so, entao colar na parede leva o drone por todo o labirinto ate
	# cair no tesouro. get_entity_type() e' Hedge em tudo, menos no tesouro.
	direcao = North
	while get_entity_type() != Entities.Treasure:
		esquerda = vira_esquerda(direcao)
		if move(esquerda):            # 1o tenta virar a esquerda
			direcao = esquerda
		elif move(direcao):           # 2o segue reto
			pass
		else:
			direita = vira_direita(direcao)
			if move(direita):         # 3o tenta virar a direita
				direcao = direita
			else:                     # 4o beco sem saida: meia-volta
				direcao = vira_direita(direita)
				move(direcao)
	harvest()   # so colhe quando esta em cima do tesouro
