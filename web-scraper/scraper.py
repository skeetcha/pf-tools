import requests
import re
import time
import json
import sys

def main():
	response = requests.get('https://aonprd.com/Races.aspx?Category=Core')

	if response.status_code != 200:
		print(f'Response status code was not 200.\n{response.status_code}\n{response.content.decode("utf-8")}')
		sys.exit(1)

	data = response.content.decode('utf-8')
	jsonData = {'classes': []}
	coreRaces = re.findall(r'<b><img src="\S+" title="[\S ]+" style="[\S ]+">([\S ]+)</a></b>', data)

	if len(coreRaces) == 0:
		print('Could not find core races.')
		sys.exit(2)

	for i in coreRaces:
		newClass = {}
		newClass['name'] = i.strip()

		classResponse = requests.get('https://aonprd.com/RacesDisplay.aspx?ItemName={}'.format(i.strip()))

		if classResponse.status_code != 200:
			print(f'Response status code was not 200.\n{classResponse.status_code}\n{classResponse.content.decode("utf-8")}')
			sys.exit(3)

		classData = classResponse.content.decode('utf-8')
		sources = re.match(r'<b>Source</b> <a href="\S+" target="\S+" class="\S+"><i>([A-z ]+) pg. ([\d]+)</i></a>(?:, <a href="\S+" target="\S+"><i>([A-z ]+) pg. (\d+)</i></a>(?:, <a href="\S+" target="\S+"><i>([A-z ]+) pg. (\d+)</i></a>)?)?', classData)

		if not firstHeading:
			print(f'List of sources not found.\n{i.strip()}')
			sys.exit(4)

		newClass['sources'] = []

		if sources.groups() == 2:
			newClass.get('sources').append({'book': sources[0], 'page': int(sources[1])})
		elif sources.groups() == 4:
			newClass.get('sources').append({'book': sources[0], 'page': int(sources[1])})
			newClass.get('sources').append({'book': sources[2], 'page': int(sources[3])})
		elif sources.groups() == 6:
			newClass.get('sources').append({'book': sources[0], 'page': int(sources[1])})
			newClass.get('sources').append({'book': sources[2], 'page': int(sources[3])})
			newClass.get('sources').append({'book': sources[4], 'page': int(sources[5])})

		time.sleep(5)

if __name__ == '__main__':
	main()

# \s*<br>\s*([A-z ,.]+)(?:&nbsp;<br><br> ([A-z ,-.;\']+)(?:&nbsp;<br><br> ([A-z ,.\-]+)(?:&nbsp;<br><br> ([A-z ,.]+))?)?)?&nbsp;<br><br> <b>Physical Description</b>: ([A-z ,.\-—]+)&nbsp;<br><br> <b>Society</b>: ([A-z \'.,\-"]+)&nbsp;<br><br> <b>Relations</b>: ([A-z ,.\-"\']+)&nbsp;<br><br> <b>Alignment and Religion</b>: ([A-z .,—]+)&nbsp;<br><br> <b>Adventurers</b>: ([A-z ,.\-]+)&nbsp;<br><br> <b>Males Names</b>: ([A-z, ]+). &nbsp;<br><br> <b>Female Names</b>: ([A-z, ]+).