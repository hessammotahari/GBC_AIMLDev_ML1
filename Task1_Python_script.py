# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import requests
import re
# Code here - Import BeautifulSoup library
from bs4 import BeautifulSoup
import sys

# Code ends here

# function to get the html source text of the medium article
def get_page():
	# Ask the user to input the article URL
	url = input("Enter url of a medium article: ").strip()

	# handling possible error
	#if not re.match(r'https?://medium.com/', url):
	#	print('Please enter a valid website, or make sure it is a medium article')
	#	sys.exit(1)

	# Call requests.get with headers
	headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://medium.com/",
}

	# fetch the page (with fallback for 403)
	def fetch_soup(url, headers, timeout=20):
		res = requests.get(url, headers=headers, timeout=timeout)
		# If Medium blocks (403), fallback to a readable proxy
		if res.status_code == 403:
			# build proxy URL without duplicating scheme
			tail = url.split('://', 1)[1] if '://' in url else url
			proxy_url = "https://r.jina.ai/http://" + tail
			res = requests.get(proxy_url, headers=headers, timeout=timeout)
		res.raise_for_status()
		return BeautifulSoup(res.text, "html.parser")

	soup = fetch_soup(url, headers)
	return soup, url

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text


def collect_text(soup, url):
	text = f'url: {url}\n\n'
	para_text = soup.find_all('p')
	for para in para_text:
		text += f"{para.text}\n\n"
	return text

# function to save file in the current directory
def save_file(text, url):
	if not os.path.exists('./scraped_articles'):
		os.mkdir('./scraped_articles')
	name = url.split("/")[-1]
	print(name)
	fname = f'scraped_articles/{name}.txt'
	
	# Code here - write a file using with (2 lines)
	with open(fname, 'w', encoding='utf-8') as f:
		f.write(text)

	# Code ends here

	print(f'File saved in directory {fname}')


if __name__ == '__main__':
	soup, url = get_page()
	text = collect_text(soup, url)
	save_file(text, url)
	# Instructions to Run this python code
	# Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7