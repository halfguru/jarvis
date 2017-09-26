from jarvis import Jarvis

if __name__ == '__main__':
	jarvis = Jarvis()
	jarvis.greetings()
	jarvis.current_time()
	#jarvis.music("play")
	robot_name = ["jarvis", "showman","charters", "garvin",
	"charges", "charles","charms","for this", "sure this", "for that","john","for you","for her", "far this"]
	while True:
		print("Waiting for command..")
		command = jarvis.listen2()
		if command is not None:
			for i in range(len(robot_name)):
				if command.lower().startswith(robot_name[i]):
					#jarvis.say(command)
					print("I heard you say: " + command.replace(robot_name[i],"Jarvis"))
					break
				elif i==len(robot_name)-1:
					print("command failed: " + str(command))

			if "play music" in command.lower():
				jarvis.music('play')

			elif "greetings" in command.lower():
				jarvis.greetings()

			elif "time" in command.lower():
				jarvis.current_time()

			command = ""