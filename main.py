import FAZENDA
import ABOBORA
import CACTO

clear()

while True:
	# crops simples: colhe + planta na mesma passada paralela
	while num_items(Items.Hay) <= 64*64:
		FAZENDA.plantar_e_colher(Entities.Grass)
	while num_items(Items.Wood) <= num_items(Items.Hay):
		FAZENDA.plantar_e_colher(Entities.Tree)
	while num_items(Items.Wood) >= 64:
		FAZENDA.plantar_e_colher(Entities.Carrot)

	# crops de bloco: usam a mecanica de fusao/ordenacao (rendem muito mais)
	while num_items(Items.Carrot) >= 64:
		ABOBORA.Abroba()
	# CACTO.Cacto()   # descomente pra farmar cacto (usa o campo inteiro)
