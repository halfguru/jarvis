self.GOOGLE_CLOUD_SPEECH_CREDENTIALS = config.GOOGLE_CLOUD_SPEECH_CREDENTIALS

def listen(self):
	with sr.Microphone() as source:
		self.r.adjust_for_ambient_noise(source)
		audio = self.r.listen(source)
	# recognize speech using Sphinx
	try:
		return self.r.recognize_sphinx(audio)
		# or: return recognizer.recognize_google(audio)
	except sr.UnknownValueError:
		print("Could not understand audio")
	except sr.RequestError as e:
		print("Recog Error; {0}".format(e))

	return ""

def listen_google(self):
	with sr.Microphone() as source:
		self.r.adjust_for_ambient_noise(source)
		audio = self.r.listen(source)
	# recognize speech using Google Cloud Speech
	try:
		print("Reading command...")
		return self.r.recognize_google_cloud(audio, credentials_json = self.GOOGLE_CLOUD_SPEECH_CREDENTIALS)
	except sr.UnknownValueError:
		print("Google Cloud Speech could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Cloud Speech service; {0}".format(e))


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
def __exit__(self, type, value, traceback):