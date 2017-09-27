import os
from jarvis import *
from functions import *
from microphone import *

if __name__ == '__main__':
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Simon/Desktop/Coding/jarvis/src/google_credentials.json"
	f = Functions()
	jarvis = Jarvis()
	jarvis.run()