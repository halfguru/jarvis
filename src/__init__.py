import os, config
from jarvis import *
from functions import *
from microphone import *

if __name__ == '__main__':
	#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CLOUD_SPEECH_CREDENTIALS_PATH
	f = Functions()
	jarvis = Jarvis()
	jarvis.run()	 