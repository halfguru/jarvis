import config, sys, time
from commands import Commands
from random import randint

class Jarvis():
	def __init__(self):
		pass
		
	def run(self):
		prev_command = ""
		c = Commands()
		c.booting()

		while True:
			command = c.listen()			
			if command is not None:					
				command = command.lower()
				if self.incomplete_command(command):	
					c.incomplete()
				else:
					for fct_keyword in config.fct_key:
						if any(self.space_words(word) in self.space_words(command) for word in fct_keyword):
							print("Command name: " + config.fct_name[config.fct_key.index(fct_keyword)])
							if config.fct_name[config.fct_key.index(fct_keyword)] == "search":
								c.search(command)
								break
							elif config.fct_name[config.fct_key.index(fct_keyword)] == "youtube":
								c.youtube(command)
								break
							else:
								getattr(c, config.fct_name[config.fct_key.index(fct_keyword)])()
								break
			time.sleep(0.5)
			prev_command = command

	#Check if command is incomplete
	def incomplete_command(self, incomplete_word):
		if any(self.space_words(word) in self.space_words(incomplete_word) for word in config.incomplete_key) and len(incomplete_word.split()) == 1:
			return True
		else:
			return False

	def space_words(self, command):
		return (' ' + command + ' ')

