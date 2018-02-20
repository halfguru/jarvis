from datetime import datetime, time
from mic import *

WORDS = ["greetings","hello","salutations","hi","hey"]
m = Mic()

def handle(text):
    now = datetime.now()
    now_time = now.time()
    if now_time >= time(1,30) and now_time <= time(12,30):
        m.say('Good morning sir')
    elif now_time >= time(12,31) and now_time <= time(17,30):
        m.say('Good afternoon sir')
    else:   
        m.say('Good evening sir')