from random import randint
from mic import *

WORDS = []
thank_you_words = ["thank you","thanks","appreciate it"]
pos_reply_words = ["interesting","amazing","wow", "cool","awesome"]
wake_up_words 	= ["you there", "hey jarvis", "wake up", "you up","hear me"]
sorry_words 	= ["sorry", "my bad", "my fault", "oops", "my mistake"]
reactions = [thank_you_words,pos_reply_words,wake_up_words, sorry_words]
for reaction in reactions:
	for word in reaction:
		WORDS.append(word)
m = Mic()


def handle(text):
	if text in thank_you_words:
		thank_you()
	elif text in pos_reply_words:
		pos_reply()
	elif text in wake_up_words:
		wake_up()
	elif text in sorry_words:
		sorry()
	else:
		print("Reaction module not responding.")

def thank_you():
	thank_you_response = ["no problem sir", "with pleasure sir", "much obliged sir"]
	choice = randint(0,len(thank_you_response)-1)
	m.say(thank_you_response[choice])

def pos_reply():
	pos_reply = ["Indubitably, sir", "Quite so, sir", "Indeed it is sir", "I am incapable of understanding emotional response but I can empathize with your amazement, sir"]
	choice = randint(0,len(pos_reply)-1)
	m.say(pos_reply[choice])

def wake_up():
	wake_up	= ["At your service sir", "Yes sir?"]
	choice = randint(0,len(wake_up)-1)
	m.say(wake_up[choice])

def sorry():
	sorry = ["no problem, sir", "mistakes are only human, sir", "you are forgiven, sir, carry on", "do not be sorry sir", "no worries", "it's fine", "apology accepted", "don't mention it","you should be, but I forgive you."]
	choice = randint(0,len(sorry)-1)
	m.say(sorry[choice])
