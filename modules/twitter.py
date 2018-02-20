import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import *
from mic import *
import sys, time, re

m = Mic()
WORDS = ["twitter"]


# Input is latest retweet, mention, direct message ID
def getNotifications(latestRetweet, latestMention, api):
    
    latestRetweets = []
    latestRetweetsID = []
    latestMentions = []
    latestMentionsID = []
    
    mentions = api.mentions_timeline()
    retweets = api.retweets_of_me()
    
    for mention in mentions:
        if mention.id > latestMention:
            latestMentions.append(mention)
            latestMentionsID.append(mention.id)

    for retweet in retweets:
        if retweet.id > latestRetweet:
            latestRetweets.append(retweet)
            latestRetweetsID.append(retweet.id)

    if len(latestRetweets) > 0:
        m.say("Latest Retweets are")
        for retweetFinal in latestRetweets:
            m.say(retweetFinal.text + " by " + retweetFinal.user.screen_name) 

        latestRetweetsID.sort()
        latestRetweet = latestRetweetsID[-1]
        retweetsIDFile = open('retweetsIDFile.txt', 'w')
        retweetsIDFile.write(str(latestRetweet))
        retweetsIDFile.close()
        
    else:
        m.say("You have no retweets")

    if len(latestMentions) > 0:
        m.say("Latest Mentions are")
        
        for mentionFinal in latestMentions:
            m.say(mentionFinal.text + " from " + mentionFinal.user.screen_name)

        latestMentionsID.sort()
        latestMention = latestMentionsID[-1]
        mentionIDFile = open('mentionIDFile.txt', 'w')
        mentionIDFile.write(str(latestMention))
        mentionIDFile.close()
    
    else:
        m.say("You have no mentions")

    
def handle(text):
    
    consumer_key        = "0x0KHvARiBjzlR08fbouzXiaX"
    consumer_secret     = "EtHnlHLe5TVShDvIPYt7pzLDeCsrFmlSktGOoOG1btOnH9Vxzt"
    access_token        = "932677356-9JaMTWfs9NauS1KgorqQRfMYHVc38FOV4HHBa9Ah"
    access_token_secret = "CaP28WN3mK6rME2CVWVivm9Auhx89ajGskrp5ZOFXRqxa"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    myTwitterID = api.me().id

    mentions = api.mentions_timeline(count=1)

    try:
        mentionIDFile = open('mentionIDFile.txt', 'r')
        latestMentionID = mentionIDFile.readline()
        latestMention = int(latestMentionID)
        mentionIDFile.close()
    except IOError:
        mentionIDFile = open('mentionIDFile.txt', 'w')
        for mention in mentions:
            latestMention = mention.id
        mentionIDFile.write(str(latestMention))
        mentionIDFile.close()

    retweets = api.retweets_of_me(count=1)

    try:
        retweetsIDFile = open('retweetsIDFile.txt', 'r')
        retweetsID = retweetsIDFile.readline()
        latestRetweet = int(retweetsID)
        retweetsIDFile.close()
    except IOError:
        retweetsIDFile = open('retweetsIDFile.txt', 'w')
        for retweet in retweets:
            latestRetweet = retweet.id
        retweetsIDFile.write(str(latestRetweet))
        retweetsIDFile.close()


    getNotifications(latestRetweet,latestMention, api)
