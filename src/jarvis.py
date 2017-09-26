from functions import Functions

class Jarvis():
	def __init__(self):
		self.robot_name = ["jarvis", "showman","charters", "garvin",
		"charges", "charles","charms","for this", "sure this", "for that","john","for you","for her", "far this"]

	def run(self):
		f = Functions()
		f.greetings()
		#f.current_time()
		#jarvis.music("play")

		"""
		while True:
			print("Waiting for command..")
			command = f.listen2()
			if command is not None:
				for i in range(len(self.robot_name)):
					if command.lower().startswith(self.robot_name[i]):
						#f.say(command)
						print("I heard you say: " + command.replace(self.robot_name[i],"f"))
						break
					elif i==len(self.robot_name)-1:
						print("command failed: " + str(command))

				if "play music" in command.lower():
					f.music('play')

				elif "greetings" in command.lower():
					f.greetings()

				elif "time" in command.lower():
					f.current_time()

				command = ""
		"""