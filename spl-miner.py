#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Seattle Public Library Web Item Crawler
# Copyright (c) 2013-2016, Byungkyu (Jay) Kang
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# USAGE: 
# 1. type the following command at the prompt
# 	$ python spl-miner.py
# 2. type the "bib number" of an item


import sys, os, codecs, json
import BeautifulSoup # easy_install beautifulsoup
import urllib
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def remove_html_tags(tags,data):
	p = re.compile(tags)
	if tags == '\n':
		return p.sub(' ', data)
	else:
		return p.sub(' ', data)


if __name__ == '__main__':	
	
	urlHead = "http://seattle.bibliocommons.com/item/show/"
	urlTail = "030"

	fname = raw_input("Please type the file name and path that contains bibnumbers to search >> ")
	f = open(fname,'r')
	fout = 'spl-output.json'

	cnt = 0
	while 1:
		l = f.readline()
		if not l:
			break

		cnt += 1
		# e.g. bibNumber = "1726706"
		bibNumber = l.strip()
								
		url = urlHead + bibNumber + urlTail
		print(url)
		data = urllib.urlopen(url)
		soup = BeautifulSoup.BeautifulSoup(data)

		#soup.prettify()
		# raw = soup.findAll('div', attrs={'id':'bibInformationContent'})
		spans = soup('span')

		texts = []

		for span in spans:
			tmp = strip_tags(str(span))
			# tmp = tmp.strip()
			tmp = tmp.replace('\n',' ')
			# if len(tmp) > 0:
			texts.append(tmp)

		count = 0
		data = {}
		data['bib']=bibNumber
		data['type']=""
		data['avg-rating']=""
		data['uni-title']=""
		data['alt-title']=""
		data['add-cont']=""
		data['dist']=""
		data['pub']=""
		data['pages']=0
		data['series']=""
		data['ed']=""
		data['isbn']=""
		data['lang']=""
		data['contents']=""
		data['perf']=""
		data['notes']=""
		data['resp']=""
		data['phy']=""
		data['auth-misc']=""
		data['call']=""
		data['ser-con']=""
		data['desc']=""

		for i in range(0,len(texts)):
			if ("(Book -" in texts[i]) and (i < 3):
				data['type'] = texts[i].strip().replace('(','').replace(')','')
			elif "Average Rating:" in texts[i]:
				data['avg-rating'] = texts[i+1].split(' ')[0]
			elif "Uniform Title" in texts[i]:
				data['uni-title'] = texts[i+1]
			elif "Alternate Title:" in texts[i]:
				data['alt-title'] = texts[i+1]
			elif "Additional Contributors:" in texts[i]:
				data['add-cont'] = texts[i+1]
			elif "Distributor:" in texts[i]:
				data['dist'] = texts[i+1]
			elif "Publisher:" in texts[i]:
				data['pub'] = texts[i+1]
			elif "Pages:" in texts[i]:
				data['pages'] = int(texts[i+1])
			elif "Series:" in texts[i]:
				data['series'] = texts[i+1]
			elif "Edition:" in texts[i]:
				data['ed'] = texts[i+1]
			elif "ISBN:" in texts[i]:
				data['isbn'] = texts[i+1]
			elif "Language:" in texts[i]:
				data['lang'] = texts[i+1]
			elif "Contents:" in texts[i]:
				data['contents'] = texts[i+1]
			elif "Performers:" in texts[i]:
				data['perf'] = texts[i+1]
			elif "Notes:" in texts[i]:
				data['notes'] = texts[i+1]
			elif "Statement of responsibility:" in texts[i]:
				data['resp'] = texts[i+1]
			elif "Physical description:" in texts[i]:
				data['phy'] = texts[i+1]
			elif "Other author misc:" in texts[i]:
				data['auth-misc'] = texts[i+1]
			elif "Call number:" in texts[i]:
				data['call'] = texts[i+1]
			elif "Series Continues:" in texts[i]:
				data['ser-con'] = texts[i+1]
			elif "Description:" in texts[i]:
				data['desc'] = texts[i+1]
			# print str(i) + ": " + texts[i]
		
		# print data
		with codecs.open(fout, "a", 'utf-8') as textFile:
			textFile.write(json.dumps(data))
			textFile.write('\n')

	print cnt, "items have been successfully crawled!\nOutput: spl-output.json\n"