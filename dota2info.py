import site_parser as sp

class Dota2info():
	"Main class responsible for obtaining info"
	def __init__(self, address):
		self.address = address

	def get_heroes_list(self, language = 'english'): #TODO: add images
		json_url = 'http://' + self.address + '/jsfeed/heropickerdata?l=' + language
		data = sp.get_json(json_url) # main data ready. 

		# From HTML, we get pics and STR/AGI/INT and Radiant/Dire types
		html_url = 'http://' + self.address + '/heroes?l=' + language
		heroes_sections_path = ['body', 'center', 'bodyContainer', 'centerColContainer', 'centerColContent', 'redboxOuter', 'redboxContent', 'heroPickerInner']
		hero_sections = sp.naviget(heroes_sections_path, sp.get_html(html_url))

		hero_specs = ('STR', 'AGI', 'INT')
		hero_sides = ('Radiant', 'Dire')
		section_names = ['heroCol' + pos for pos in ('Left', 'Middle', 'Right')]

		for (spec, section_name) in zip(hero_specs, section_names):
			thus_named_sections = hero_sections.find_all(class_=section_name)
			for (side, section) in zip(hero_sides, thus_named_sections):
				for hero_item in section.find_all('a'):
					id = hero_item['id'][5:] # link_invoker -> invoker
					data[id]['icon_small'] = sp.naviget('heroHoverSmall', hero_item)['src']
					data[id]['icon'] = sp.naviget('heroHoverLarge', hero_item)['src']
					data[id]['spec'] = spec
					data[id]['side'] = side

		return data

	def get_hero_details(self, hero_id, language = 'english'):
		raise NotImplementedError
	def get_items_list(self, language = 'english'):
		raise NotImplementedError
	def get_item_details(self, item_id, language = 'english'):
		raise NotImplementedError

