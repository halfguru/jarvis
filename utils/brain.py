import pkgutil, config, importlib, sys
from mic import *

class Brain():

    def __init__(self):
        self.mic = Mic()

    def loop(self):
        while True:
            voice_input = self.mic.listen()
            if voice_input is not None:
                voice_input = voice_input.lower()
                self.module_find_keyword(voice_input)

    def listen_command(self):
        while True:
            voice_input = self.mic.listen()
            if voice_input is not None:
                voice_input = voice_input.lower()
                return voice_input


    def module_find_keyword(self, voice_input):
        modules = []
        for file in os.listdir(config.MODULES_PATH):
            if file.endswith(".py"):
                file = file.replace(".py","")
                modules.append(file)
                mod = __import__(file)
                for word in mod.WORDS:
                    if self.space_words(word) in self.space_words(voice_input):
                        mod.handle(voice_input)

    def space_words(self, command):
        return (' ' + command + ' ')
