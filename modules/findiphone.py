import re, sys, os, time
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
from mic import *

WORDS = ["find", "iphone", "phone", "ring"]

# SHOULD PROBABLY BE GLOBAL IN JASPER
AFFIRMATIVE = ["YES", "YEAH", "SURE", "YAH", "YA"]
NEGATIVE = ["NO", "NEGATIVE", "NAH", "NA", "NOPE"]

# Retrieve password
with open(config.UTILS_PATH + "\\utils\\apple_config.txt","r") as apple_config:
    password = apple_config.read()

# iCloud Settings
ICLOUD_USERNAME = "miss_ya182@hotmail.com"
ICLOUD_PASSWORD = password

m = Mic()

def handle(text):
    m.say("Are you sure you want to use the iphone function?")
    voice_input = m.listen()
    if voice_input is not None:
        voice_input = voice_input.lower()

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
        if "iPhone" in current["deviceDisplayName"]:
            iphones.append(device)

    # No iphones
    if len(iphones) == 0:
        m.say("No IPhones Found on your account")
        return

    # Many iphones
    i = 0 
    if len(iphones) > 1:
        m.say("There are multiple iphones on your account.")
        for phone in iphones:
            m.say("Did you mean the {type} named {name}?".format(type=phone.status()['deviceDisplayName'], name=phone.status()['name']))
            voice_input = m.listen()
            if voice_input is not None:
                voice_input = voice_input.lower()
                if "yes" in voice_input:
                    phone_to_ring = iphones[i]
                    break
                else:
                    i+=1

    # Just one
    phone_to_ring = iphones[1]

    if not phone_to_ring:
        m.say("You didn't select an iPhone")
        return
 
    m.say("Sending ring command to the phone now")
    time.sleep(3)
    phone_to_ring.play_sound()

if __name__ == '__main__':
    handle("phone")