import urllib.request, json
from bs4 import BeautifulSoup
from collections import Iterable

def get_json(url):
	response = urllib.request.urlopen(url).read().decode('utf8')
	data = json.loads(response)
	return data
	
def get_html(url):
	response = urllib.request.urlopen(url).read().decode('utf8')
	data = BeautifulSoup(response)
	return data

def naviget(query, subject): 
	def simple_get(field, subject):
		try:
			return subject[field]
		except KeyError:
			pass
		except TypeError:
			pass
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

def naviget_all(query, subjects):
	if not isinstance(subjects, Iterable):
		subjects = [subject]
	if isinstance(query, str):
		query = [query]

	def elementary_get_all(term, subject):
		try:
			by_name = subject.find_all(term)
			by_id = subject.find_all(id=term)
			by_class = subject.find_all(class_=term)
			return by_name + by_id + by_class
		except AttributeError:
			return []

	for term in query:
		term_getter = lambda sub: elementary_get_all(term, sub)
		subjects = [item for sublist in map(term_getter, subjects) for item in sublist]
	return subjects
