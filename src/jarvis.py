import config, sys, time
from functions import Functions
from random import randint

class Jarvis():
	def __init__(self):
		pass
		
	def run(self):
		f = Functions()
		f.say("How may I be of assistance sir?")
		prev_command = ""
		while True:
			command = f.listen()
			if command is not None:
				command = command.lower()

				if any(word in command for word in config.greetings_list):
					f.greetings()
				elif any(word in command for word in config.wake_up_list):
					f.wake_up()
				elif any(word in command for word in config.exit_list):
					f.exit()
				elif any(word in command for word in config.enum_command_list):
					f.enum_command()
				elif any(word in command for word in config.time_list):
					f.current_time()
				elif any(word in command for word in config.weather_list):
					f.weather()
				elif any(word in command for word in config.music_list):
					f.music("play")
				elif any(word in command for word in config.mission_list):
					f.say(config.mission)
				elif any(word in command for word in config.master_list):
					f.say(config.master)
				elif any(word in command for word in config.search_list):
					if "search" in command:
						f.search(command.split("search",1)[1].lstrip())
					if "look up" in command:
						f.search(command.split("look up",1)[1].lstrip())
				elif any(word in command for word in config.search_more_list) and \
					 any(word in prev_command for word in config.search_list) :
					f.search(prev_command.split("search",1)[1].lstrip(),4)
				elif "youtube" in command:
					f.youtube(command.replace("youtube",""))
				elif any(word in command for word in config.thank_you_list):
					choice = randint(0,len(config.thank_you)-1)
					f.say(config.thank_you[choice])
				elif any(word in command for word in config.sorry_list):
					choice = randint(0,len(config.sorry)-1)
					f.say(config.sorry[choice])

				time.sleep(0.5)
				prev_command = command



