import wikipedia
from mic import *

WORDS = ["search", "look up", "define"]
m = Mic()

def handle(text):
    for key in WORDS:
        if key in text:
            text = text.split(key,1)[1].lstrip()
            break
    try:
        m.say("Searching for " + str(text))
        if text is not "":
            print("Searching for " + str(text))
            search_summary = ".".join(wikipedia.summary(text).split(".")[:(1)])
            m.say(search_summary)
        else:
            m.say("Your search query is empty sir")
    except:
        m.say("Please precise your search query sir")