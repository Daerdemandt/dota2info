import urllib.request, json
from bs4 import BeautifulSoup

class Dota2info:
	"Main class responsible for obtaining info"
	def __init__(self, address):
		self.address = address

	def get_heroes_list(self, language = 'english'): #TODO: add images
		json_url = 'http://' + self.address + '/jsfeed/heropickerdata?l=' + language
		data = self.get_json(json_url)
		html_url = 'http://' + self.address + '/heroes?l=' + language
		heroes_sections_path = ['body', 'center', 'bodyContainer', 'centerColContainer', 'centerColContent', 'redboxOuter', 'redboxContent', 'heroPickerInner']
		heroSections = self.naviget(heroes_sections_path, self.get_html(html_url))
		return heroSections


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
	
	def get_html(self, url):
		response = urllib.request.urlopen(url).read().decode('utf8')
		data = BeautifulSoup(response)
		return data
	
	def naviget(self, query, subject):
		def simple_get(field, subject):
			if hasattr(subject, field):
				return getattr(subject, field)
			return subject
			return subject.find(id='bodyContainer')
			return subject.find(id=field)
		if isinstance(query, str):
			query = [query]
		for term in query:
			subject = simple_get(term, subject)
		return subject

	def naviget(self, query, subject): #TODO: if nothing is found by is, look by class
		def simple_get(field, subject):
			if hasattr(subject, field) and getattr(subject, field):
				return getattr(subject, field)
			return subject.find(id=field)
		if isinstance(query, str):
			query = [query]

		for term in query:
			subject =  simple_get(term, subject)
		return subject

