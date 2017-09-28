import pyttsx3, os, json, config, math, urllib.parse, webbrowser, wikipedia
import speech_recognition as sr
from microphone import *
from random import randint
from weather import Weather
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime, time
from random import randint

class Functions():
	def __init__(self):
		self.r = sr.Recognizer()
		self.engine = pyttsx3.init()
		self.rate = self.engine.getProperty('rate')
		self.voices = self.engine.getProperty('voices')
		self.engine.setProperty('rate', self.rate - 20)
		self.engine.setProperty('voice', self.voices[1].id)
		self.language_code = 'en-US'  # a BCP-47 language tag
		self.client = speech.SpeechClient()
		self.config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=RATE, language_code=self.language_code)
		self.streaming_config = types.StreamingRecognitionConfig(config=self.config,interim_results=True)

	#Open microphone and listen for input
	def listen(self):
		with MicrophoneStream(RATE, CHUNK) as stream:
			audio_generator = stream.generator()
			requests = (types.StreamingRecognizeRequest(audio_content=content)for content in audio_generator)
			responses = self.client.streaming_recognize(self.streaming_config, requests)
			# Now, put the transcription responses to use.
			print("Awaiting command")
			print("----------------")
			return self.listen_print_loop(responses)

	#Iterates through server responses and prints them.
	def listen_print_loop(self, responses):
		num_chars_printed = 0
		try:
			for response in responses:
				print("Debug6")
				if not response.results:
					print("Debug1")
					continue
				# The `results` list is consecutive. 
				result = response.results[0]

				if not result.alternatives:
					print("Debug2")
					continue
				# Display the transcription of the top alternative.
				print("Debug3")
				transcript = result.alternatives[0].transcript
				# Display interim results, but with a carriage return at the end of the
				# line, so subsequent lines will overwrite them.
				overwrite_chars = ' ' * (num_chars_printed - len(transcript))

				if not result.is_final:
					print("Debug4")
					sys.stdout.write(transcript + overwrite_chars + '\r')
					sys.stdout.flush()
					num_chars_printed = len(transcript)

				else:
					print("Debug5")					
					print(transcript + overwrite_chars)
					# Exit recognition if any of the transcribed phrases could be
					# one of our keywords.
					if re.search(r'\b(exit|quit)\b', transcript, re.I):
						print('Exiting..')
						break
					num_chars_printed = 0
					return (transcript + overwrite_chars)
		except KeyboardInterrupt:
			print ('Interrupted')
			try:
				sys.exit(0)
			except SystemExit:
				os._exit(0)
		except:
			print("No commands detected in 1 minute")

	#Change voice
	def voice_change(self, voice):
		self.engine.setProperty('voice', self.voices[int(voice)].id)
		self.say("Here is my new voice. I hope you enjoy it.")

	#Change voice speed
	def voice_speed(self, speed):
		self.engine.setProperty('rate',self.rate+speed)

	#Voice says something
	def say(self, voice_command):
		print("Jarvis says: " + str(voice_command))
		self.engine.say(str(voice_command))
		self.engine.runAndWait()

	#List choices for voice change
	def voice_change_command(self):
		self.say("Which voice would you like to select sir?")
		command = self.listen()
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

	#Greetings depending on time
	def greetings(self,):
		now = datetime.now()
		now_time = now.time()
		if now_time >= time(1,30) and now_time <= time(12,30):
			self.say('Good morning sir')
		elif now_time >= time(12,31) and now_time <= time(17,30):
			self.say('Good afternoon sir')
		else:   
			self.say('Good evening sir')

	#Notifies the user the system is present
	def wake_up(self,):
		choice = randint(0,len(config.wake_up)-1)
		self.say(config.wake_up[choice])

	#Close system
	def exit(self,):
		self.say(config.exit)
		sys.exit()

	#Checks current hour and minute
	def current_time(self):
		now = datetime.now()    
		self.say("It is currently")
		self.say(str(now.hour) + " hour")
		self.say(str(now.minute) + " minute")

	#Plays music
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

	#Checks weather
	def weather(self):
		weather = Weather()
		lookup = weather.lookup(91982014)
		condition = lookup.condition()
		condition['temp'] = str(math.ceil((int(condition['temp']) - 32)*0.555555))
		self.say("It is currently " + condition['temp'] + " degrees celcius and condition is " + condition['text'])

	def youtube(self, textToSearch):
		self.say("Searching for video")
		query = urllib.parse.quote(textToSearch)
		url = "https://www.youtube.com/results?search_query=" + query
		response = urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html,"html.parser")
		self.say("Playing" + str(textToSearch) + " youtube video")
	
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
			if "https://googleads.g.doubleclick.net/" not in vid['href']:
				print ("https://www.youtube.com" + vid["href"])
				webbrowser.open("https://www.youtube.com" + vid["href"])
				break

	def search(self, search_wiki, search_length=1):
		try:
			self.say("Searching for " + str(search_wiki))
			if search_wiki is not "":
				print("Searching for " + str(search_wiki))
				search_summary = ".".join(wikipedia.summary(search_wiki).split(".")[:(search_length)])
				self.say(search_summary)
			else:
				self.say("Your search query is empty sir")
		except:
			self.say("Please precise your search query sir")

	def enum_command(self):
		self.say("Here is the list of commands I can accomplish for you sir")
		for commands in config.enum_command:
			self.say(commands)