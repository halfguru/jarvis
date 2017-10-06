import math
from weather import Weather
from mic import *


WORDS = ["weather", "temperature", "outside", "out there", "forecast"]
m = Mic()

def handle(text):
	weather = Weather()
	lookup = weather.lookup(91982014)
	condition = lookup.condition()
	condition['temp'] = str(math.ceil((int(condition['temp']) - 32)*0.555555))
	m.say("It is currently " + condition['temp'] + " degrees celcius and condition is " + condition['text'])