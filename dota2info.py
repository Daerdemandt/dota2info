import urllib.request, json
from bs4 import BeautifulSoup
from collections import namedtuple, Iterable

class Dota2info:
	"Main class responsible for obtaining info"
	def __init__(self, address):
		self.address = address

	def get_heroes_list(self, language = 'english'): #TODO: add images
		json_url = 'http://' + self.address + '/jsfeed/heropickerdata?l=' + language
		data = self.get_json(json_url) # main data ready. 

		# From HTML, we get pics and STR/AGI/INT and Radiant/Dire types
		html_url = 'http://' + self.address + '/heroes?l=' + language
		heroes_sections_path = ['body', 'center', 'bodyContainer', 'centerColContainer', 'centerColContent', 'redboxOuter', 'redboxContent', 'heroPickerInner']
		hero_sections = self.naviget(heroes_sections_path, self.get_html(html_url))

		hero_specs = ('STR', 'AGI', 'INT')
		hero_sides = ('Radiant', 'Dire')
		section_names = ['heroCol' + pos for pos in ('Left', 'Middle', 'Right')]

		for (spec, section_name) in zip(hero_specs, section_names):
			thus_named_sections = hero_sections.find_all(class_=section_name)
			for (side, section) in zip(hero_sides, thus_named_sections):
				for hero_item in section.find_all('a'):
					id = hero_item['id'][5:] # link_invoker -> invoker
					data[id]['icon_small'] = self.naviget('heroHoverSmall', hero_item)['src']
					data[id]['icon'] = self.naviget('heroHoverLarge', hero_item)['src']
					data[id]['spec'] = spec
					data[id]['side'] = side

		return data

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
			if hasattr(subject, field) and getattr(subject, field):
				return getattr(subject, field)
			by_id = subject.find(id=field)
			if (None != by_id):
				return by_id
			return subject.find(class_=field)
		if isinstance(query, str):
			query = [query]

		for term in query:
			subject =  simple_get(term, subject)
		return subject

	def naviget_all(self, query, subjects):
		if not isinstance(subjects, Iterable):
			subjects = [subject]
		if isinstance(query, str):
			query = [query]

		def elementary_get_all(term, subject):
			by_name = subject.get_all(term)
			by_id = subject.get_all(id=term)
			by_class = subject.get_all(class_=term)
			return by_name + by_id + by_class

		for term in query:
			term_getter = lambda sub: elementary_get_all(term, sub)
			subjects = sum(map(term_getter, subjects))
		return subjects
