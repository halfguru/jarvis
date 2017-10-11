import vlc, sys, os, pathlib, time, platform
from random import randint
from mic import *

WORDS = []
music_play_words    = ["music play", "play music"]
music_pause_words 	= ["pause music", "music pause", "pause","resume", "resume music"]
music_stop_words 	= ["stop", "stop music", "music stop"]
music_selection		= ["music selection", "music list", "list music"]
music_list = [music_play_words, music_pause_words, music_stop_words, music_selection]
for music in music_list:
	for word in music:
		WORDS.append(word)

def handle(text):
	if text in music_play_words:
		p.OnOpen()
	if text in music_pause_words:
		p.PlayPause()
	if text in music_stop_words:
		p.OnStop()
	if text in music_selection:
		p.OnMusicList()

class Player():
	def __init__(self):
		# basic vlc instance
		self.Instance = vlc.Instance() 
		# empty vlc media player
		self.player = self.Instance.media_player_new()

	def OnOpen(self):
		# Stop if music is playing
		if self.player.is_playing():
			self.player.stop()
		#Select random music
		music_key = []
		for root, dirs, files in os.walk('E:\music'):
			for filename in files:
				if os.path.splitext(filename)[1] == ".mp3":
					music_key.append(os.path.join(root, filename))
		randomSong = randint(0,len(music_key))

		# create the media
		self.media = self.Instance.media_new(music_key[randomSong])
		# put the media in the media player
		self.player.set_media(self.media)

		# parse the metadata of the file
		self.media.parse()
		# Report info of the file chosen
		title = self.player.get_title()
		duration = self.player.get_length() / 1000
		mm, ss = divmod(duration, 60)
		print ("Playing", music_key[randomSong], "Length:", "%02d:%02d" % (mm,ss))

		self.PlayPause()

	def OnStop(self):
		print("Music stopped")
		self.player.stop()

	def PlayPause(self):
		if self.player.is_playing():
			print("Music paused")
			self.player.pause()
			self.isPaused = True
		else:
			print("Music resumed")
			self.player.play()
			self.isPaused = False

	def OnMusicList(self):
		#Select random music
		music_key = []
		music_filenames = []
		i = 0
		for root, dirs, files in os.walk('E:\music'):
			for filename in files:
				if os.path.splitext(filename)[1] == ".mp3":
					if i >=3:
						break
					music_key.append(os.path.join(root, filename))
					music_filenames.append(filename.replace(".mp3", ""))
					i+=1
		m.say("Here is a short selection of songs in your current music library sir.")
		m.say(music_filenames)
		m.say("Which song would you like to select?")
		voice_input = m.listen()
		if voice_input is not None:
			voice_input = voice_input.lower()
			if "one" in voice_input:
				self.media = self.Instance.media_new(music_key[0])
				print(music_key[0])
			if "two" in voice_input:
				self.media = self.Instance.media_new(music_key[1])
				print(music_key[1])
			if "three" in voice_input:
				self.media = self.Instance.media_new(music_key[2])	
				print(music_key[2])

		# put the media in the media player
		self.player.set_media(self.media)
		self.PlayPause()


	def OnTimer(self):

		if self.player == None:
			return
		# since the self.player.get_length can change while playing,
		length = self.player.get_length()
		dbl = length * 0.001

		# update the time on the slider
		tyme = self.player.get_time()
		if tyme == -1:
			tyme = 0
		dbl = tyme * 0.001


	def volume_sel(self, evt):
		if self.player == None:
			return
		volume = self.volume_var.get()
		if volume > 100:
			volume = 100
		if self.player.audio_set_volume(volume) == -1:
			print("Failed to set volume")

	def OnToggleVolume(self, evt):
	
		is_mute = self.player.audio_get_mute()
		self.player.audio_set_mute(not is_mute)

	def OnSetVolume(self):
		"""Set the volume according to the volume sider.
		"""
		volume = self.volume_var.get()
		# vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
		if volume > 100:
			volume = 100
		if self.player.audio_set_volume(volume) == -1:
			self.errorDialog("Failed to set volume")
m = Mic()
p = Player()