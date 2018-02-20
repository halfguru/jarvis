
import sys
import os
current_path = os.getcwd()
sys.path.append(current_path + "/utils")
sys.path.append(current_path + "/modules")
import config
from jarvis import *
from mic import *

if __name__ == '__main__':
    jarvis = Jarvis()
    jarvis.run()
