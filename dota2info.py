class Dota2info:
	"Main class responsible for obtaining info"
	def __init__(self, address):
		pass
	def get_heroes_list(self, language = 'english'):
		raise NotImplementedError
	def get_hero_details(self, hero_id, language = 'english'):
		raise NotImplementedError
	def get_items_list(self, language = 'english'):
		raise NotImplementedError
	def get_item_details(self, item_id, language = 'english'):
		raise NotImplementedError
