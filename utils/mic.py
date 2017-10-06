#!/usr/bin/env python
from __future__ import division
import speech_recognition as sr
import re, sys, config, pyaudio, os, pyttsx3
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
	"""Opens a recording stream as a generator yielding the audio chunks."""
	def __init__(self, rate, chunk):
		self._rate = rate
		self._chunk = chunk

		# Create a thread-safe buffer of audio data
		self._buff = queue.Queue()
		self.closed = True

	def __enter__(self):
		self._audio_interface = pyaudio.PyAudio()
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paInt16,
			# The API currently only supports 1-channel (mono) audio
			# https://goo.gl/z757pE
			channels=1, rate=self._rate,
			input=True, frames_per_buffer=self._chunk,
			# Run the audio stream asynchronously to fill the buffer object.
			# This is necessary so that the input device's buffer doesn't
			# overflow while the calling thread makes network requests, etc.
			stream_callback=self._fill_buffer,
		)

		self.closed = False

		return self

	def __exit__(self, type, value, traceback):
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		# Signal the generator to terminate so that the client's
		# streaming_recognize method will not block the process termination.
		self._buff.put(None)
		self._audio_interface.terminate()

	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		"""Continuously collect data from the audio stream, into the buffer."""
		self._buff.put(in_data)
		return None, pyaudio.paContinue

	def generator(self):
		while not self.closed:
			# Use a blocking get() to ensure there's at least one chunk of
			# data, and stop iteration if the chunk is None, indicating the
			# end of the audio stream.
			chunk = self._buff.get()
			if chunk is None:
				return
			data = [chunk]

			# Now consume whatever other data's still buffered.
			while True:
				try:
					chunk = self._buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break

			yield b''.join(data)

class Mic():
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

	#Voice says something
	def say(self, voice_command):
		print("Jarvis says: " + str(voice_command))
		self.engine.say(str(voice_command))
		self.engine.runAndWait()
# [END audio_stream]