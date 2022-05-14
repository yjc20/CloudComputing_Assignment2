#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 17:12:45 2022

@author: archit
"""

import json
from dbconnector import Couch
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")


# ip address for the master node from ip.txt file
ip_file=open("ip.txt", "r")
couchdb_master_ip=ip_file.readline().rstrip()
ip_file.close()


# couchdb connection class instance created
couch=Couch('http://'+couchdb_master_ip+':5984/',['tweet'])

def preprocess(text):
    text = re.sub("@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+", ' ', str(text).lower()).strip()
    return text

def subjectivity(text):
    text = preprocess(text)
    subjectivity = TextBlob(text).sentiment.subjectivity
    return subjectivity
    
    
def polarity(text):
    sia = SentimentIntensityAnalyzer()
    text = preprocess(text)
    polarity = sia.polarity_scores(text)['compound']
    return polarity


try :
    f = open('tweets.json')
    file = json.load(f)
    tweets_collector = []
    
    for i in file['rows']:
        tweet = {"tweet_id":i['tweet_id'], "text":i["text"],"city":i["city"],"subjectivity":subjectivity(i["text"]),
                 "polarity":polarity(i["text"]), "retweet_count":i["retweet_count"], "favorite_count":i["favorite_count"]}
        tweets_collector.append(tweet)

    counter = 0
    for i in tweets_collector:
        couch.pushdata(i,'tweet')
        if(counter %5000 == 0):
          print(i)
        counter += 1  

            
except:
    pass
