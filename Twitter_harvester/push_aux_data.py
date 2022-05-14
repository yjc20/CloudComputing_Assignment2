#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 17:12:45 2022

@author: archit
"""

import json
from dbconnector import Couch



# ip address for the master node from ip.txt file
ip_file=open("ip.txt", "r")
couchdb_master_ip=ip_file.readline().rstrip()
ip_file.close()


# couchdb connection class instance created
couch=Couch('http://'+couchdb_master_ip+':5984/',['tweet'])


try :
    f = open('tweets.json')
    file = json.load(f)
    tweets_collector = []
    
    for i in file['rows']:
        tweet = {"tweet_id":i['tweet_id'], "text":i["text"],"city":i["city"]}
        tweets_collector.append(tweet)
    
    counter = 0
    for i in tweets_collector:
        couch.pushdata(i,'tweet')
        if(counter %5000 == 0):
          print(i)
        counter += 1  

            
except:
    pass
