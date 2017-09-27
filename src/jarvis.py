from functions import Functions
from random import randint
import config

class Jarvis():
	def __init__(self):
		pass
	def run(self):
		f = Functions()

		f.say("How may I be of assistance sir?")

		while True:
			command = f.listen()
			if command is not None:
				command = command.lower()
			if any(word in command for word in config.greetings_list):
				f.greetings()
			elif any(word in command for word in config.time_list):
				f.current_time()
			elif any(word in command for word in config.music_list):
				f.music("play")
			elif any(word in command for word in config.mission_list):
				f.say(config.mission)
			elif any(word in command for word in config.thank_you_list):
				choice = randint(0,len(config.thank_you)-1)
				f.say(config.thank_you[choice])
			elif any(word in command for word in config.sorry_list):
				choice = randint(0,len(config.sorry)-1)
				f.say(config.sorry[choice])
			elif any(word in command for word in config.master_list):
				f.say(config.master)
			elif any(word in command for word in config.weather_list):
				f.weather()
			prev_command = command



