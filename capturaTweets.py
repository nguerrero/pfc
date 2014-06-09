#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
from pymongo import MongoClient

import twitter
import json
import sys
from urllib2 import URLError
#pymongo
#mongoengine
#api twitter


#Programa principal
access_token ="1205614682-ZKyLfynUuaMXqwrjlz3z8btO3YbkS8CMusEv1Tf"
access_token_secret = "WYYDpQqiEwK92Hh3PI7ZGJan1hWldYckXYfX2PDeQ"
consumer_key ="BIYC56i5GKzCyTYlgur9YA"
consumer_secret="1TPGvGaFfJl6bHSVOKBZpAJm1koNrLjeX0iUOMmE"
ip = 'localhost'
port = 6000

# Me registro en twitter
auth = twitter.oauth.OAuth(access_token, access_token_secret,consumer_key, consumer_secret)
api = twitter.Twitter(domain='api.twitter.com',api_version='1.1',auth=auth)

# Pongo el streaming
twitter_stream = twitter.TwitterStream(auth=api.auth)
stream = twitter_stream.statuses.filter(track = "a")
print 'Escuchando...'
for tweet in stream:
	# Recibo tweet
	print 'Conecto con la bd'
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	#tweetCollection.insert(tweet)
	print 'Dentro tweet y cierro conexion'
	client.close()
	print tweet

print 'Registro completado con exito'


print 'Conectado con la bbdd...'
#mongoengine.insert({_id: 101, username:"iloveyou", age: 12, likes: "destroy your computer"})




