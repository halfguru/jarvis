import pyttsx3, os, json, config, math, urllib.parse, webbrowser, wikipedia, imaplib, email
import speech_recognition as sr
from microphone 	import *
from random     	import randint
from weather 		import Weather
from bs4 			import BeautifulSoup
from urllib.request import urlopen
from datetime 		import datetime, time
from random 		import randint

class Commands():

	def __init__(self):
		#Jarvis voice
		self.r = sr.Recognizer()
		self.engine = pyttsx3.init()
		self.rate = self.engine.getProperty('rate')
		self.voices = self.engine.getProperty('voices')
		self.engine.setProperty('rate', self.rate - 20)
		self.engine.setProperty('voice', self.voices[1].id)
		self.language_code = 'en-US'  # a BCP-47 language tag

		#Speech Recognizer
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CLOUD_SPEECH_CREDENTIALS_PATH
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
			print("=======================================================")
			print("                 waiting for command...                ")
			print("=======================================================")
			return self.listen_print_loop(responses)

	#Iterates through server responses and prints them.
	def listen_print_loop(self, responses):
		num_chars_printed = 0
		try:
			for response in responses:
				if not response.results:
					continue
				# The `results` list is consecutive. 
				result = response.results[0]

				if not result.alternatives:
					continue
				# Display the transcription of the top alternative.
				transcript = result.alternatives[0].transcript
				# Display interim results, but with a carriage return at the end of the
				# line, so subsequent lines will overwrite them.
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
						sys.exit(0)
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

	#Booting up message
	def booting(self):
		import time
		self.say(config.booting_message[0])
		time.sleep(1)
		self.say(config.booting_message[1])

	#Incomplete command detection
	def incomplete(self):
		self.say(config.incomplete)

	#Creator name
	def master(self):
		self.say(config.master)



	#Jarvis states its purpose	
	def mission(self):		
		self.say(config.mission)


	def gmail(self):
		ORG_EMAIL   = "@gmail.com"
		FROM_EMAIL  = "dkhoe7" + ORG_EMAIL
		FROM_PWD    = "philosophiagc23ba"
		SMTP_SERVER = "imap.gmail.com"
		SMTP_PORT   = 993
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		mail.login(FROM_EMAIL,FROM_PWD)
		mail.select('inbox')

		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]

		id_list = mail_ids.split()   
		print(id_list[0])
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])


		for i in range(latest_email_id,first_email_id, -1):
			typ, data = mail.fetch(str(i), '(RFC822)' )

			for response_part in data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1].decode('utf-8'))
					email_subject = msg['subject']
					email_from = msg['from']
					print ('From : ' + email_from + '\n')
					print ('Subject : ' + email_subject + '\n')



	def enum_command(self):
		self.say("Here is the list of commands I can accomplish for you sir")
		for commands in config.enum_command:
			self.say(commands)

if __name__ == '__main__':
	c = Commands()
	c.gmail()