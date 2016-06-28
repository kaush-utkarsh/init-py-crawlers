import requests
from bs4 import BeautifulSoup
import time
import os
import sqlite3

flag = 0

conn = sqlite3.connect('../data/dsgnblog.db')

c = conn.cursor()

try:
	c.execute('''
		CREATE TABLE seeds
		(
			source varchar(200),
			seed varchar(1000) UNIQUE,
			page_number int,
		)
	''')
except:
	pass

page_count = 1
g = open('../seeds/dsgn_blog_seeds.txt', 'w')

while True:
	print page_count
	
	r = requests.get('http://thedsgnblog.com/page/' + str(page_count))
	soup = BeautifulSoup(r.text)

	divs = soup.findAll('div', {'class': 'entry'})

	if divs:
		for i in divs:
			div_details = i.find('div', {'class': 'details'})
			link = div_details.find('a')
			g.write(link['href'] + os.linesep)

			source = 'dsgnblog'
			seed = link['href']
			try:
				c.execute("INSERT INTO seeds VALUES (?, ?, ?)", (source, seed, page_count))
				conn.commit()
			except:
				conn.close()
				exit()
	else:
		break
		
	page_count = page_count + 1
	time.sleep(1)

conn.close()