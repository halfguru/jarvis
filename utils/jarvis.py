import config, sys, time, diagnose
from brain import *
from mic import *

class Jarvis():
	def __init__(self):
		pass
		
	def run(self):
		print("*******************************************************")
		print("*                       JARVIS                        *")
		print("*            (c) 2017 Simon Dang Khoa Ho              *")
		print("*******************************************************")

		#Check if Internet is ruining since Google speech recognition requires it
		if not diagnose.check_network_connection():
			print("Network not connected. This may prevent Jasper from running properly.")

		m = Mic()
		m.say("Jarvis system on.")
		time.sleep(1)
		m.say("How may I be of service sir?")
		b = Brain()
		b.loop()
"""

	#Check if command is incomplete
	def incomplete_command(self, incomplete_word):
		if any(self.space_words(word) in self.space_words(incomplete_word) for word in config.incomplete_key) and len(incomplete_word.split()) == 1:
			return True
		else:
			return False


	def space_words(self, command):
		return (' ' + command + ' ')
"""

