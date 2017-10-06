import urllib.parse, webbrowser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from mic import *

WORDS = ["youtube", "video"]
m = Mic()

def handle(text):
	for key in WORDS:
		if key in text:
			text = text.split(key,1)[1].lstrip()
			break
	m.say("Searching for video")
	query = urllib.parse.quote(text)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html,"html.parser")
	m.say("Playing " + str(text) + " youtube video")

	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		if "https://googleads.g.doubleclick.net/" not in vid['href']:
			print ("https://www.youtube.com" + vid["href"])
			webbrowser.open("https://www.youtube.com" + vid["href"])
			break
