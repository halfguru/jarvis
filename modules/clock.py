from datetime import datetime, time
from mic import *

WORDS = ["time", "hour"]
m = Mic()

def handle(text):
    now = datetime.now()    
    m.say("It is currently")
    m.say(str(now.hour) + " hour")
    m.say(str(now.minute) + " minute")
