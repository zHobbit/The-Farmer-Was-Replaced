import Utilidades

# ============================================================================
# plantar_e_colher(tipo): numa unica passada paralela (todos os drones), em cada
# casa faz TUDO de uma vez -> prepara o solo, planta se vazia, fertiliza (se a
# regra deixar) e, se ficou pronta, colhe e ja replanta. Visitar a casa uma vez
# so e' o que maximiza a eficiencia.
# ============================================================================

def precisa_solo(tipo):
	# cenoura, abobora, cacto e girassol crescem em solo arado; o resto em grama
	return (tipo == Entities.Carrot or tipo == Entities.Pumpkin
		or tipo == Entities.Cactus or tipo == Entities.Sunflower)


def plantar_e_colher(tipo):
	Utilidades.trocar_chapeu(Hats.Brown_Hat)
	fert = Utilidades.pode_fertilizar()      # decide 1x por passada (drone principal)

	def tratar():
		# 1) garante o solo certo pro tipo
		if precisa_solo(tipo):
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()
		# 2) planta se a casa estiver vazia
		if get_entity_type() == None:
			plant(tipo)
		# 3) fertiliza -> fica pronta na hora
		if fert:
			Utilidades.Fertilizar()
		# 4) colhe se estiver pronta e ja replanta (mesma visita)
		if can_harvest():
			harvest()
			plant(tipo)
		# 5) rega culturas de solo (cada drone rega as suas)
		if precisa_solo(tipo) and get_water() < 0.5:
			use_item(Items.Water)

	Utilidades.for_all(tratar)
