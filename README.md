## JARVIS

Just A Rather Very Intelligent System. JARVIS is a personal project to create a system with voice recognition (google-cloud) to make commands. The user can also easily create custom commands in the modules folder and following the correct structure.

### Prerequisites

Python3 & pip
```
python -m pip install -U pip
pip install google-cloud
pip install pyttsx3
pip install webbrowser
pip install wikipedia
pip install SpeechRecognition
pip install bs4
```

### Building
```
python __init__.py
```


## Custom modules

In modules, create another python file. Here's the clock module as an example:

```
from datetime import datetime, time
from mic import *

# Words the system will recognize
WORDS = ["time", "hour"] 
# Instantiate the microphone
m = Mic()

# JARVIS action after saying one of the WORDS
def handle(text):
	now = datetime.now()    
	m.say("It is currently")
	m.say(str(now.hour) + " hour")
	m.say(str(now.minute) + " minute")
```

## Built With

* [Python3](https://www.python.org/download/releases/3.0/) - Programming language

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Ironman
