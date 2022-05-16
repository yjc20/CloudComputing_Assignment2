# -*- coding: utf-8 -*-

import tweepy
from tweepy import OAuthHandler
import os
import re
import time
from dbconnector import Couch
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")



# ip address for the master node from ip.txt file
ip_file=open("ip.txt", "r")
while True:
    couchdb_master_ip=ip_file.readline().rstrip()
    if couchdb_master_ip != '':         #checking to not get an empty string
        break
ip_file.close()


# couchdb connection class instance created
couch=Couch('http://'+couchdb_master_ip+':5984/',['tweet'])

# Getting various tweetapi from database
api=couch.getdata('apikey')

#authentication for twitter
api_key = api['Api_Key']
api_secret = api['Api_Secret_Key']
access_token = api['Access_Token']
access_token_secret = api['Access_Secret_Token']

authorizer = OAuthHandler(api_key, api_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer, timeout=15, wait_on_rate_limit=True)


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

# Getting tweets 
while True:
    
    
    # code fetching from db
    location=couch.getdata('subregion')
    place=location['code']
    


    #tweets collection
    tweets_collector = []
  
    try:
        
        
        for tweet in tweepy.Cursor(api.search_tweets, q="place:%s" % place, lang='en', result_type='recent', tweet_mode='extended').items(10000):
            tweets_collector.append({"tweet_id":str(tweet.id), "text":str(tweet.full_text),"city":str(tweet.place.name),
                                     "subjectivity":subjectivity(tweet.full_text), "polarity":polarity(tweet.full_text),
                                     "retweet_count":tweet.retweet_count, "favorite_count":tweet.favorite_count})
#Handling twitter duplication           
#         else:
#             for tweet in tweepy.Cursor(api.search, q="place:%s" % geo +" since_id:%s" % curr_since_id, lang='en', result_type='recent', tweet_mode='extended').items(10000000):
#                 all_tweets.append({"id":str(tweet.id), "uid":str(tweet.user.id), "text":str(tweet.full_text), "created_at":str(tweet.created_at), "city":str(tweet.place.name), "country":str(tweet.place.country), "box":str(tweet.place.bounding_box.coordinates), "sentiment":str(senti.sentiment_analysis(tweet.full_text)[0][1])})
    

        counter = 0
        # Pushing tweets to db
        for i in tweets_collector:
            couch.pushdata(i,'tweet')
            if(counter %100 == 0):
              print(i)
            counter += 1  
        
#         if all_tweets:
#             couch.updatesinceid('code',geo,all_tweets[0]['id'])
            
    except:
        pass

    # Reset the flag in region database
    couch.resetflag('code',place,'subregion')
    del(tweets_collector)
    #print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(40)
