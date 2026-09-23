import Utilidades

def Abroba():
	# replanta em paralelo ate o campo inteiro fundir numa abobora gigante, ai colhe.
	Utilidades.trocar_chapeu(Hats.Pumpkin_Hat)
	while not can_harvest():
		fert = Utilidades.pode_fertilizar()  # decide 1x por passada (drone principal)

		def plantar():
			# so replanta casa vazia ou abobora morta (nao mexe nas vivas que ainda crescem).
			# plantar em cima de morta remove ela automaticamente.
			if get_entity_type() != Entities.Pumpkin:
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Pumpkin)
			if fert:
				Utilidades.Fertilizar()      # acelera: o campo funde mais rapido

		Utilidades.for_all(plantar)
	harvest()
