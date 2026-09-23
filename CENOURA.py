import Utilidades

def Cenora():
	Utilidades.trocar_chapeu(Hats.Carrot_Hat)
	fert = Utilidades.pode_fertilizar()      # decide 1x por passada (drone principal)

	def tratar():
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() == None:
			plant(Entities.Carrot)
		if fert:
			Utilidades.Fertilizar()          # fica pronta na hora
		if can_harvest():
			harvest()
			plant(Entities.Carrot)           # ja deixa a proxima crescendo
		if get_water() < 0.5:                # cada drone rega so as proprias casas
			use_item(Items.Water)

	Utilidades.for_all(tratar)
