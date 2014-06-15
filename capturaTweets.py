#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
from pymongo import MongoClient

import twitter
import json
import sys
from urllib2 import URLError
import contrasenas
#pymongo
#mongoengine
#api twitter


#Programa principal
ip = 'localhost'
port = 6000

# Me registro en twitter
auth = twitter.oauth.OAuth(contrasenas.access_token, contrasenas.access_token_secret,contrasenas.consumer_key, contrasenas.consumer_secret)
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




