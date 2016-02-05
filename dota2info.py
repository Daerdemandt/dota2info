import urllib.request, json


class Dota2info:
	"Main class responsible for obtaining info"
	def __init__(self, address):
		self.address = address

	def get_heroes_list(self, language = 'english'): #TODO: add images
		url = 'http://' + self.address + '/jsfeed/heropickerdata?l=' + language
		return self.get_json(url)

	def get_hero_details(self, hero_id, language = 'english'):
		raise NotImplementedError
	def get_items_list(self, language = 'english'):
		raise NotImplementedError
	def get_item_details(self, item_id, language = 'english'):
		raise NotImplementedError

	def get_json(self, url):
		response = urllib.request.urlopen(url).read().decode('utf8')
		data = json.loads(response)
		return data
