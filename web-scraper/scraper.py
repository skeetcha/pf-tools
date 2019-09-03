import requests
import re
from bs4 import BeautifulSoup
import time
import sys

def main():
	raceCategories = ['Core', 'NonCore']

	jsonData = {}

	for raceCategory in raceCategories:
		raceCategoryResponse = requests.get(f'https://aonprd.com/Races.aspx?Category={raceCategory}')

		if raceCategoryResponse.status_code != 200:
			print(f'Response status code was not 200.\n{raceCategoryResponse.status_code}\n{raceCategoryResponse.content.decode("utf-8")}')
			sys.exit(1)

		raceCategoryData = raceCategoryResponse.content.decode('utf-8')
		raceCategorySoup = BeautifulSoup(raceCategoryData)

		if 'races' not in jsonData.keys():
			jsonData['races'] = []

		for i in raceCategorySoup.find_all('a'):
			raceRe = re.search(r'[A-z]+\.[a-z]+\?ItemName=([A-z\-]+)', i.get('href'))

			if raceRe:
				newRace = getRaceData(raceRe.group(1))

			time.sleep(5)

		time.sleep(5)

def getRaceData(race):
	raceResponse = requests.get(f'https://aonprd.com/RacesDisplay.aspx?ItemName={race}')

	if raceResponse.status_code != 200:
		print(f'Response status code was not 200.\n{raceResponse.status_code}\n{raceResponse.content.decode("utf-8")}')
		sys.exit(2)

	raceData = raceResponse.content.decode('utf-8')
	raceSoup = BeautifulSoup(raceData)

	newRace = {}

	row = raceSoup.table.tr.td
	data = str(row).split('<br/>')

	# data[0] - Sources
	sourceSoup = BeautifulSoup(data[0])

	for i in sourceSoup.find_all('a'):
		sourceRe = re.search(r'([A-z ]+) pg. (\d+)', sourceSoup.find_all('a')[0].i.string)

		if sourceRe:
			if 'sources' not in newRace.keys():
				newRace['sources'] = []

			newRaces.get('sources').append({'book': sourceRe.group(1), 'page': int(sourceRe.group(2))})

	# data[1:X] - Background Info
	i = 1

	while True:
		if 'Physical Description' in data[i]:
			break

		if data[i]:
			if 'info' not in newRace.keys():
				newRace['info'] = []

			newRace.get('info').append(data[i].strip())

		i += 1

	# data[X + 1] - Physical Description
	newRace['descriptions'] = {}
	newRace.get('descriptions')['physical'] = re.sub(r'<b>Physical Description</b>: *', '', data[i]).strip()
	i += 1

	if not data[i]:
		i += 1

	# data[X + 2] - Society Description
	newRace.get('descriptions')['society'] = re.sub(r'<b>Society</b>: *', '', data[i]).strip()
	i += 1

	if not data[i]:
		i += 1

	# data[X + 3] - Relations
	newRace.get('descriptions')['relations'] = re.sub(r'<b>Relations</b>: *', '', data[i]).strip()
	i += 1

	if not data[i]:
		i += 1

	# data[X + 4] - Alignment and Religion
	newRace.get('descriptions')['alrelig'] = re.sub(r'<b>Alignment and Religion</b>: *', '', data[i]).strip()
	i += 1

	if not data[i]:
		i += 1

	# data[X + 5] - Adventurers
	newRace.get('descriptions')['adventurers'] = re.sub(r'<b>Adventurers</b>: *', '', data[i]).strip()
	i += 1

	if not data[i]:
		i += 1

	# data[X + 6] - Male Names
	newRace['names'] = {}
	newRace.get('names')['male'] = re.sub(r'<b>Males Names</b>: *', '', data[i]).strip().replace('.', '').split(', ')
	i += 1

	if not data[i]:
		i += 1

	# data[X + 7] - Female Names
	newRace.get('names')['female'] = re.sub(r'<b>Female Names</b>: *', '', data[i]).strip().split('.')[0].split(', ')

	# data[X + 7] - Ability Score Modifiers
	amods = re.findall(r'(\+|\u2013|\-)(\d+) *([A-z]+)', BeautifulSoup(data[i].replace(data[i].split('.')[0], '')[1:]).b.string)

	if not amods:
		print(f'Ability modifiers not found.\n{data[i].replace(data[i].split(".")[0], "")[1:]}')
		sys.exit(2)

	for mod in amods:
		if 'abilityMods' not in newRace.keys():
			newRace['abilityMods'] = []

		if ord(mod[0]) == 8211:
			newRace.get('abilityMods').append({'mod': int(mod[1]) * -1, 'ability': mod[2]})
		else:
			newRace.get('abilityMods').append({'mod': int(mod[1]), 'ability': mod[2]})

	# data[X + 7] - Ability Score Modifier Description
	desc = re.search(r'<b>[A-z\+\d ,–]+</b>: *([A-z ,\.]+)', data[i].replace(data[i].split('.')[0], '')[1:])

	if not desc:
		print(f'Ability modifier description not found.\n{data[i].replace(data[i].split(".")[0], "")[1:]}')
		sys.exit(3)

	newRace['traits'] = {}

	newRace.get('traits')['abilityMod'] = desc.group(1)

if __name__ == '__main__':
	main()