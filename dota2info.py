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

		hero_classes = ('STR', 'AGI', 'INT')
		hero_sides = ('Radiant', 'Dire')
		section_names = ['heroCol' + pos for pos in ('Left', 'Middle', 'Right')]

		for (hero_class, section_name) in zip(hero_classes, section_names):
			thus_named_sections = hero_sections.find_all(class_=section_name)
			for (side, section) in zip(hero_sides, thus_named_sections):
				for hero_item in section.find_all('a'):
					id = hero_item['id'][5:] # link_invoker -> invoker
					data[id]['icon_small'] = sp.naviget('heroHoverSmall', hero_item)['src']
					data[id]['icon'] = sp.naviget('heroHoverLarge', hero_item)['src']
					data[id]['class'] = hero_class
					data[id]['side'] = side

		return data

	def get_hero_details(self, hero_id, language = 'english'):
		hero_data = {
			'id': hero_id,
			'name':hero_id.replace('_', ' ').title()
		}
		hero_page_url = 'http://' + self.address + '/hero/' + hero_id.title().replace("'S_", "s_")
		html_content_path = ['body', 'center', 'bodyContainer', 'centerColContainer', 'centerColContent']
		html_data = sp.naviget(html_content_path, sp.get_html(hero_page_url))
		def parse_range(x):
			low, high = (piece.strip() for piece in x.split('-'))
			return {'string':x, 'min':low, 'max':high}

		def parse_progression(x):
			base, increment = (piece.strip() for piece in x.split('+'))
			return {'string':x, 'base':base, 'increment':increment}

		def parse_vision(x):
			day, night = (piece.strip() for piece in x.split('/'))
			return {'string':x, 'day':day, 'night':night}

		extract = lambda path: sp.naviget(path, html_data)
		title = extract(['h1', 'string'])
		hsh = lambda s: s.lower().replace(' ', '').replace('_', '').replace("'", '')
		if (hsh(title) != hsh(hero_data['name'])):
			return {'error':'invalid hero id'}
		block_update = lambda mapping, block: hero_data.update({key: sp.naviget(mapping[key], block) for key in mapping})
		block_update(
			{
				'image':['heroTopPortraitContainer', 'img', 'src'],
				'spec':['heroBioRoles', 'bioTextAttack', 'string'],
				'roles':['heroBioRoles', 'bioTextAttack', 'nextSibling'],
			},
			html_data
		)
		hero_data['roles'] = hero_data['roles'].split(' - ')[1:] # to remove empty element

		blocks = sp.naviget_all(['redboxOuter', 'redboxContent'], [html_data])

		blocks = {name : sp.naviget(name + 'Inner', block) for (name, block) in zip(['overview', 'bio', 'stats', 'abilities'], blocks)}

		block_update(
			{
				'portrait' : ['overviewHeroLeft', 'heroPrimaryPortraitHolder', 'img', 'src'],
				'int' : ['overviewPrimaryStats', 'overview_IntVal', 'string'],
				'agi' : ['overviewPrimaryStats', 'overview_AgiVal', 'string'],
				'str' : ['overviewPrimaryStats', 'overview_StrVal', 'string'],
				'attack' : ['overviewPrimaryStats', 'overview_AttackVal', 'string'],
				'speed' : ['overviewPrimaryStats', 'overview_SpeedVal', 'string'],
				'defense' : ['overviewPrimaryStats', 'overview_DefenseVal', 'string'],
			},
			blocks['overview']
		)
		hero_data['attack'] = parse_range(hero_data['attack'])
		for growing_stat in ['int', 'agi', 'str']:
			hero_data[growing_stat] = parse_progression(hero_data[growing_stat])

		block_update({'bio':'text'}, blocks['bio'])
		hero_data['bio'] = hero_data['bio'].strip()

		stat_pieces = sp.naviget_all(['statsRight', 'div', 'statRowCol2W'], [blocks['stats']])
		for (piece, name) in zip(stat_pieces, ['vision_range', 'attack_range', 'missile_speed']):
			hero_data[name] = piece.string
		hero_data['vision_range'] = parse_vision(hero_data['vision_range'])

		hero_data['stats_by_level'] = sp.parse_div_table(sp.naviget('statsLeft', blocks['stats']))
		hero_data['stats_by_level']['Damage'] = [parse_range(x) for x in hero_data['stats_by_level']['Damage']]
		hero_data['stats_by_level']['Mana'] = [int(x.replace(',', '')) for x in hero_data['stats_by_level']['Mana']]

		self.ensure_abilities()
		if hero_id == 'natures_prophet':
			hero_data['abilities'] = self.hero_abilities['furion']
		else:
			hero_data['abilities'] = self.hero_abilities[hero_id]

		return hero_data
	
	def retreive_abilities(self):
		#TODO: languages
		#TODO: fancy parsing of those
		whole_bunch  = sp.get_json('http://www.dota2.com/jsfeed/heropediadata?feeds=abilitydata&l=russian')['abilitydata']
		heroes = set(sp.get_json('http://www.dota2.com/jsfeed/heropickerdata?l=russian').keys())
		hero_abilities = {hero : {} for hero in heroes}
		for ability_name_full in whole_bunch:
			ability_name_words = ability_name_full.split('_')
			for word_count in range(1, len(ability_name_words)):
				hero_id = '_'.join(ability_name_words[:word_count])
				if hero_id in heroes:
					break
			ability = whole_bunch[ability_name_full]
			if hero_id not in heroes:
				hero_id = ability['hurl'].lower()
			hero_abilities[hero_id][ability['dname']] = ability
		self.hero_abilities = hero_abilities
	
	def ensure_abilities(self):
		if hasattr(self, 'hero_abilities'):
			return
		self.retreive_abilities()

	def get_items_list(self, language = 'english'):
		raise NotImplementedError
	def get_item_details(self, item_id, language = 'english'):
		raise NotImplementedError
	

