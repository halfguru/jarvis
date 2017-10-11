import re, sys, os
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
from mic import *

WORDS = ["find", "iphone", "phone", "ring"]

# SHOULD PROBABLY BE GLOBAL IN JASPER
AFFIRMATIVE = ["YES", "YEAH", "SURE", "YAH", "YA"]
NEGATIVE = ["NO", "NEGATIVE", "NAH", "NA", "NOPE"]

# iCloud Settings
ICLOUD_USERNAME = "miss_ya182@hotmail.com"
ICLOUD_PASSWORD = "Xiangdingdang9876"

m = Mic()

def handle(text):
	"""
		Makes your iPhone ring
		Arguments:
		text -- user-input, typically transcribed speech
		mic -- used to interact with the user (for both input and output)
		profile -- contains information related to the user (e.g., phone
				   number)
	"""
	try:
		api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
	except PyiCloudFailedLoginException:
		m.say("Invalid Username & Password")
		return

	# All Devices
	devices = api.devices

	# Just the iPhones
	iphones = []

	# The one to ring
	phone_to_ring = None

	for device in devices:
		current = device.status()
		if "iPhone" in current['deviceDisplayName']:
			iphones.append(device)

	"""
	# Many iphones
	elif len(iphones) > 1:
		m.say("There are multiple iphones on your account.")
		for phone in iphones:
			m.say("Did you mean the {type} named {name}?".format(type=phone.status()['deviceDisplayName'], name=phone.status()['name']))
			command = m.activeListen()
			if any(aff in command for aff in AFFIRMATIVE):
				phone_to_ring = phone
				break
	"""

	# No iphones
	if len(iphones) == 0:
		m.say("No IPhones Found on your account")
		return

	# Just one
	phone_to_ring = iphones[1]

	if not phone_to_ring:
		m.say("You didn't select an iPhone")
		return

	m.say("Sending ring command to the phone now")
	phone_to_ring.play_sound()

if __name__ == '__main__':
	handle("phone")