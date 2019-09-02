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

if __name__ == '__main__':
	main()