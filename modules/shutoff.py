from mic import *

WORDS = ["exit", "terminate", "close","power down"]
m = Mic()

def handle(text):
	m.say("System powering down")
	sys.exit()