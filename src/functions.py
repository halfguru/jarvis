import pyttsx3, os
import speech_recognition as sr
from datetime import datetime, time
from random import randint
#randint from weather import Weather

class Functions():
	def __init__(self):
		# obtain audio from the microphone
		self.r = sr.Recognizer()
		self.engine = pyttsx3.init()
		self.rate = self.engine.getProperty('rate')
		self.voices = self.engine.getProperty('voices')
		self.engine.setProperty('rate', self.rate-20)
		self.engine.setProperty('voice', self.voices[0].id)

	def voice_change_command(self):
		self.say("Which voice would you like to select sir?")
		command = self.listen_google()
		if command is not None:
			command = command.lower()
			print(str(command))
			if "one" in command or "first" in command:
				self.say("You selected the first voice.")
				self.voice_change(0)
			elif "two" in command or "second" in command or "middle" in command:
				self.say("You selected the second voice.")
				self.voice_change(1)
			elif "three" in command or "third" in command or "last" in command:
				self.say("You selected the third voice.")
				self.voice_change(2)
			else:
				self.say("I am sorry. I'm afraid I couldn''t understand your answer.")
		else:
			self.say("You didn't say anything sir.")

	def voice_change(self, voice):
		self.engine.setProperty('voice', self.voices[int(voice)].id)
		self.say("Here is my new voice. I hope you enjoy it.")

	def voice_speed(self, speed):
		self.engine.setProperty('rate',self.rate+speed)

	def say(self, voice_command):
		self.engine.say(str(voice_command))
		self.engine.runAndWait()

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
		GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "idyllic-formula-181105",
  "private_key_id": "cec9a42799530df96e2c0d0fb172f747580f1559",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDJQfXD8HBlm6Mm\npRoZuaRXDWkEP8udq5hp1Ig+o1vg/91usWQFJnMVT1/CG0NikcHrOFcxh4sLmeIN\nZ3DrNZinkXXmgOvnl5uGQ95QlxbPQPfzA8BSf9tfdRUhOpy5x2rlzA6MSa39zjTg\nFlRUn6aWIJ/ai0WWLq3YXSAgnyZkO10I4ti9RyI4TecojOMSLMAUiYSmT2n6PkEC\nWHCzhdRoBo5H7+b/GJw3N6oYga3daRHjRbfyqdghtG7AfLgr7CpECh9qOvepBIVG\nERYi6BeczqjDu8kNDb/8Gt5R2tJp+EbWbPu6C58SQkYkxIWc3tVzvVrg8E9kHO+n\nT4X2sbXjAgMBAAECggEAIXdW7fn4RA/RMva8XtpoXKjDCu0C0llQ6F7qOE7uKH1+\nQvm7fJcWsaH3y0LA/fiSivyHlJm0l5LDV2BD6NDfmBRk9cCqubbo/+F0QT7GkQ3S\nzUsVOtgTpg1wRzdvDVN++pm9MjskSXKgh0IfTCJvee0QjS+gkXx59bhn7xTCi7hU\neGXwhm0bS8krVllQm8y2Z6Ur26azY9b/6V+GnKcxdDQDhNKw50fCD53L00Z1JC60\ng9vHVr4KSSo6F2NVjYb779wdJdXuHwz5a/lruxb9r69wPvmTGgSgLuESVEV/8SlO\nyHMwDAT4rU7SfTV5U6WpYr+InxQjgFbz/6GJ2q3Y2QKBgQDsyAO44Ztg92Iz7STW\nYN7wA3D8pcteATIrbP9IY+tZ+dXdOYb7mzoYrZ70STohBPId4z+Ye/jLULdjAmbT\n0thj7AbVxatgH/2bpzlpLXz6+2jNR2eZlAeZ070yyzn8ZQfns/J2GvR69FtH0Nm6\niF+I6UBKyMIoc8Q+3CAw+WnkeQKBgQDZl9BEq+cpfz0t6rQqP9HVrjeGBW2NokU9\nV0Bj/EMj9HsMAFJ19bFrPjWwhsanUwk28Zr36Yuf3VgpPI/zvt7MuanRhfNO1NN0\n1i3T3wC8DyH6Y9YBksDCkF6s3FjAyJzCzfF+4u2Dtd1x/Qx0dVq+ERrlvdsFEsP/\nOFOiNOr+OwKBgQCZbGzFAiJs7T7LiLCi3Df4azJt8nvY2IuKieDMJjpcnb7OzrTB\nGW7GiNGDVmN8+7hqV1Jg2ot2KkH5vJemT2t5K3muUJvf+Dqa/fr8RMZD1l2tDcR6\nRem66fEhFX/oJArAPuAvWP3rIaR330MFU9IbY5AOJRFxprmVRYryUNoleQKBgQCh\n/zy3Y6Q+aNSLkul/avQ2OfZseS4O/HjAKm1uAymZYzMYxESgPcNRLIecXTsY5+E8\nXrQZTm79HjW8vbIOrlQB51he/XMfhaPIoIyN6MELQdjyKdHyaefI8uMJnyMUpEbR\nYbIh3aEnJgcwDk1vhs+AIgv8b1TYehghszXQ1cT+cQKBgQDfpP5wlwD3bgNwoPV4\nsyHxUPRtRDtgNwJ3MzSfxYiUXizsVGfhqj3EHwXsXYMVKThLtt51LnckBSfvqSC/\nER5WxQZJGQWpqxWH5aRj0/+u7rfi78ZSiFXPlOOf4pSsC8Et/Hy4LOlEnDOpoaza\nEpl+7shOUo2D2YINcSx26+0Djg==\n-----END PRIVATE KEY-----\n",
  "client_email": "jarvis@idyllic-formula-181105.iam.gserviceaccount.com",
  "client_id": "103879130766032642544",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jarvis%40idyllic-formula-181105.iam.gserviceaccount.com"
}
"""
		try:
			print("Reading command...")
			return self.r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
		except sr.UnknownValueError:
			print("Google Cloud Speech could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Cloud Speech service; {0}".format(e))

	def greetings(self,):
		now = datetime.now()
		now_time = now.time()
		if now_time >= time(1,30) and now_time <= time(12,30):
			self.say('Good morning sir')
		elif now_time >= time(12,31) and now_time <= time(17,30):
			self.say('Good afternoon sir')
		else:	
			self.say('Good evening sir')

	def current_time(self):
		now = datetime.now()	
		self.say("It is currently")
		self.say(str(now.hour) + "hour")
		self.say(str(now.minute) + "minute")

	def music(self, type):
		if type.lower()=="play":
			music_list = []
			for root, dirs, files in os.walk('E:\music'):
				for filename in files:
					if os.path.splitext(filename)[1] == ".mp3":
						music_list.append(os.path.join(root, filename))
		randomSong = randint(0,len(music_list))
		path = music_list[randomSong]
		path = path.rstrip(os.sep)
		path = os.path.basename(path)
		self.say("Playing " + str(path).replace("mp3",""))
		print("Playing " + str(path).replace("mp3",""))
		os.startfile(music_list[randomSong])



	#say('Hello, my name is Jarvis. I am an artifcial intelligence designed for your assistance. How may I help you?')
	#say('Currently analyzing this sequence...')

