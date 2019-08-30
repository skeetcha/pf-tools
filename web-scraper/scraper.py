import requests
import re
import time
import json
import sys

def main():
	raceCategories = ['Core', 'NonCore']

	for category in raceCategories:
		response = requests.get(f'https://aonprd.com/Races.aspx?Category={category}')

		if response.status_code != 200:
			print(f'Response status code was not 200.\n{response.status_code}\n{response.content.decode("utf-8")}')
			sys.exit(1)

		data = response.content.decode('utf-8')
		jsonData = {'classes': []}
		races = re.findall(r'<b><img src="\S+" title="[\S ]+" style="[\S ]+">([\S ]+)</a></b>', data)

		if len(races) == 0:
			print(f'Could not find {category} races.')
			sys.exit(2)

		for race in races:
			newRace = {}
			newRace['name'] = race.strip()

			raceResponse = requests.get(f'https://aonprd.com/RacesDisplay.aspx?ItemName={race.strip()}')

			if raceResponse.status_code != 200:
				print(f'Response status code was not 200.\n{raceResponse.status_code}\n{raceResponse.content.decode("utf-8")}')
				sys.exit(3)

			raceData = raceResponse.content.decode('utf-8')
			oneSource = re.search(r'<b>Source</b>\s*<a\s*(?:href="\S+")?\s*(?:target="\S+")?\s*(?:class="\S+")?>(?:<i>)?([A-z ]+)\s*pg\.\s*(\d+)(?:</i>)?</a>', raceData)
			twoSources = re.search(r'<b>Source</b>\s*<a\s*(?:href="\S+")?\s*(?:target="\S+")?\s*(?:class="\S+")?>(?:<i>)?([A-z ]+)\s*pg\.\s*(\d+)(?:</i>)?</a>,\s*<a (?:href="\S+")?\s*(?:target="\S+")?\s*(?:class="\S+")?>(?:<i>)?([A-z ]+)\s*pg\.\s*(\d+)(?:</i>)?</a>', raceData)
			threeSources = re.search(r'<b>Source</b>\s*<a\s*(?:href="\S+")?\s*(?:target="\S+")?\s*(?:class="\S+")?>(?:<i>)?([A-z ]+)\s*pg\.\s*(\d+)(?:</i>)?</a>,\s*<a (?:href="\S+")?\s*(?:target="\S+")?\s*(?:class="\S+")?>(?:<i>)?([A-z ]+)\s*pg\.\s*(\d+)(?:</i>)?</a>,\s*<a\s*(?:href="\S+")?\s*(?:target="\S+")?\s*(?:class="\S+")?>(?:<i>)?([A-z ]+)\s*pg\.\s*(\d+)(?:</i>)?</a>', raceData)
			info = re.search(r'</a><br>([A-z ,\.]+)(?:&nbsp;<br><br>\s*([A-z ,\-\.;\']+)(?:&nbsp;<br><br>\s*([A-z ,\.\-]+)(?:&nbsp;<br><br>\s*([A-z ,\.]+))?)?)?', raceData)
			newRace['sources'] = []

			if threeSources:
				newRace.get('sources').append({'book': threeSources.group(1).strip(), 'page': int(threSources.group(2))})
				newRace.get('sources').append({'book': threeSources.group(3).strip(), 'page': int(threSources.group(4))})
				newRace.get('sources').append({'book': threeSources.group(5).strip(), 'page': int(threeSources.group(6))})
			elif twoSources and not threeSources:
				newRace.get('sources').append({'book': twoSources.group(1).strip(), 'page': int(twoSources.group(2))})
				newRace.get('sources').append({'book': twoSources.group(3).strip(), 'page': int(twoSources.group(4))})
			elif oneSource and not twoSources and not threeSources:
				newRace.get('sources').append({'book': oneSource.group(1).strip(), 'page': int(oneSource.group(2))})

			'''if not info:
				print(f'Info not found.\n{race.strip()}')
				sys.exit(5)'''

			breakpoint()

			time.sleep(5)

		time.sleep(5)

if __name__ == '__main__':
	main()