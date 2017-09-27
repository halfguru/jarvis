import pyttsx3, os, json, config, math
import speech_recognition as sr
from microphone import *
from weather import Weather
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
		self.config = types.RecognitionConfig(
			encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
			sample_rate_hertz=RATE,
			language_code=self.language_code)
		self.streaming_config = types.StreamingRecognitionConfig(
			config=self.config,
			interim_results=True)

	def listen(self):
		with MicrophoneStream(RATE, CHUNK) as stream:
			audio_generator = stream.generator()
			requests = (types.StreamingRecognizeRequest(audio_content=content)
						for content in audio_generator)

			responses = self.client.streaming_recognize(self.streaming_config, requests)
			# Now, put the transcription responses to use.
			print("Awaiting command...")
			return self.listen_print_loop(responses)

	def listen_print_loop(self, responses):
		"""Iterates through server responses and prints them.
		The responses passed is a generator that will block until a response
		is provided by the server.
		Each response may contain multiple results, and each result may contain
		multiple alternatives; for details, see https://goo.gl/tjCPAU. 
		"""
		num_chars_printed = 0
		for response in responses:
			if not response.results:
				continue
			# The `results` list is consecutive. For streaming, we only care about
			# the first result being considered, since once it's `is_final`, it
			# moves on to considering the next utterance.
			result = response.results[0]
			if not result.alternatives:
				continue
			# Display the transcription of the top alternative.
			transcript = result.alternatives[0].transcript
			# Display interim results, but with a carriage return at the end of the
			# line, so subsequent lines will overwrite them.
			#
			# If the previous result was longer than this one, we need to print
			# some extra spaces to overwrite the previous result
			overwrite_chars = ' ' * (num_chars_printed - len(transcript))

			if not result.is_final:
				sys.stdout.write(transcript + overwrite_chars + '\r')
				sys.stdout.flush()
				num_chars_printed = len(transcript)

			else:
				print(transcript + overwrite_chars)
				# Exit recognition if any of the transcribed phrases could be
				# one of our keywords.
				if re.search(r'\b(exit|quit)\b', transcript, re.I):
					print('Exiting..')
					break
				num_chars_printed = 0
				return (transcript + overwrite_chars)

	def voice_change(self, voice):
		self.engine.setProperty('voice', self.voices[int(voice)].id)
		self.say("Here is my new voice. I hope you enjoy it.")

	def voice_speed(self, speed):
		self.engine.setProperty('rate',self.rate+speed)

	def say(self, voice_command):
		print("Jarvis says: " + str(voice_command))
		self.engine.say(str(voice_command))
		self.engine.runAndWait()


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

	def weather(self):
		weather = Weather()
		lookup = weather.lookup(91982014)
		condition = lookup.condition()
		condition['temp'] = str(math.ceil((int(condition['temp']) - 32)*0.555555))
		self.say("It is currently " + condition['temp'] + "celcius and condition is " + condition['text'])

