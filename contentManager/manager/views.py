#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################
# @Author : Nazareth Guerrero Yebenes                                    #
# @Date : 			                                                     #
# @Description : Views that handle the urls selected for manager app     #
##########################################################################

# Variable to debug
DEBUG = True

# Libraries.
# HTTP mssages.
from django.http import HttpResponse,HttpResponseNotFound
from django.http import HttpResponseRedirect,HttpResponseNotAllowed

# HTML short way for rendering.
from django.shortcuts import render_to_response

# HTML rendering libraries.
from django.template.loader import get_template
from django.template import Context
#twitter library
import twitter
import json
import sys
from urllib2 import URLError

# Data base tables.
from pymongo import MongoClient

#map/reduce
from bson.code import Code
from pymongo import Connection

# ----------------------------------------------------------------------
# Name : INDEX
# To render correctly the main view (home).
access_token ="1205614682-ZKyLfynUuaMXqwrjlz3z8btO3YbkS8CMusEv1Tf"
access_token_secret = "WYYDpQqiEwK92Hh3PI7ZGJan1hWldYckXYfX2PDeQ"
consumer_key ="BIYC56i5GKzCyTYlgur9YA"
consumer_secret="1TPGvGaFfJl6bHSVOKBZpAJm1koNrLjeX0iUOMmE"
#ip = '193.147.53.153'
ip = 'localhost'
#port = 6000
port = 4567

def index(request):
	# Me registro en twitter
	#auth = twitter.oauth.OAuth(access_token_key,access_token_secret,consumer_key, consumer_secret)
	#api = twitter.Twitter(domain='api.twitter.com',api_version='1.1',auth=auth)
	#print 'Registro completado con exito'

	# return the template.
	return render_to_response('search.html', locals())

def search(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	collectionAux = db['tweetsAux']
	for aux in tweetCollection.find(limit = 10).sort('_id',-1):
		collectionAux.insert(aux)
	statuses = collectionAux.find(limit = 10).sort('_id',-1)
	db.drop_collection('tweetsAux');
	client.close()
	#return the template
	return render_to_response('search.html', locals())

def stream(request):
	#Código de mongodb
	print 'hola'
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	statuses = tweetCollection.find(limit = 10).sort('_id',-1)
	client.close()
	#return the template
	return render_to_response('search.html', locals())

def statistics(request):
	#return the template
	return render_to_response('statistics.html', locals())

def rtStatistics(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	result = tweetCollection.map_reduce(mapRT, reduceRT,"myresult",limit = 1000, sort = {'_id': -1 } )
	for doc in result.find():
		result.update({'_id':doc['_id']}, {'$set': {'text':doc['_id']}})
	rts = result.find(limit=10).sort('value',-1)
	rtArray = []
	for rt in rts:
		rtArray.append(rt['value'])
	rts = result.find(limit=10).sort('value',-1)
	client.close()
	return render_to_response('rtStatistics.html', locals())

def userStatistics(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	result2 = tweetCollection.map_reduce(mapUser, reduce,"myresult2", limit = 1000)
	for doc in result2.find():
		result2.update({'_id':doc['_id']}, {'$set': {'user':doc['_id']}})
	users = result2.find(limit=10).sort('value',-1)
	userArray = []
	for user in users:
		userArray.append(user['value'])
	users = result2.find(limit=10).sort('value',-1)
	client.close()
	#return the template
	return render_to_response('userStatistics.html', locals())

def htStatistics(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	print '1'
	result4 = tweetCollection.map_reduce(mapHT, reduce,"myresult4", limit = 1000)
	print '2'
	for doc in result4.find():
		result4.update({'_id':doc['_id']}, {'$set': {'user':doc['_id']}})
		print doc
	print '3'
	hts = result4.find(limit=10).sort('value',-1)
	htArray = []
	for ht in hts:
		htArray.append(ht['value'])
	hts = result4.find(limit=10).sort('value',-1)
	client.close()
	#return the template
	return render_to_response('htStatistics.html', locals())

def popularStatistics(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	result3 = tweetCollection.map_reduce(mapPopular, reduce,"myresult3", limit = 1000)
	for doc in result3.find():
		result3.update({'_id':doc['_id']}, {'$set': {'user':doc['_id']}})
	users = result3.find(limit=10).sort('value',-1)
	userArray = []
	for user in users:
		userArray.append(user['value'])
	users = result3.find(limit=10).sort('value',-1)
	client.close()
	#return the template
	return render_to_response('popularStatistics.html', locals())



def datesStatistics(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	# Tweets por días
	result2 = tweetCollection.map_reduce(mapCuentaDias, reduce,"myresult5")
	for doc in result2.find():
		result2.update({'_id':doc['_id']}, {'$set': {'date':doc['_id']}})
	mes = result2.find(limit=6).sort('date',-1)
	mesArray = []
	for m in mes:
		mesArray.append(m['value'])
	mes = result2.find(limit=6).sort('date',-1)
	# Tweets por días
	result3 = tweetCollection.map_reduce(mapCuentaDiasRT, reduce,"myresult7")
	for doc in result3.find():
		result3.update({'_id':doc['_id']}, {'$set': {'date':doc['_id']}})
	mesRT = result3.find(limit=6).sort('date',-1)
	mesArrayRT = []
	for m in mesRT:
		mesArrayRT.append(m['value'])
	mesRT = result3.find(limit=6).sort('date',-1)
	return render_to_response('datesStatistics.html', locals())


def yearStatistics(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	#Tweets por meses
	result = tweetCollection.map_reduce(mapCuentaMeses, reduce,"myresult6")
	for doc in result.find():
		result.update({'_id':doc['_id']}, {'$set': {'date':doc['_id']}})
	anio = result.find(limit=10).sort('date',1)
	anioArray = []
	for a in anio:
		anioArray.append(a['value'])
	anio = result.find(limit=10).sort('date',1)
	# Retweets
	result2 = tweetCollection.map_reduce(mapCuentaMesesRT, reduce,"myresult6")
	for doc in result2.find():
		result2.update({'_id':doc['_id']}, {'$set': {'date':doc['_id']}})
	anioRT = result2.find(limit=10).sort('date',1)
	anioArrayRT = []
	for a in anioRT:
		anioArrayRT.append(a['value'])
	anioRT = result2.find(limit=10).sort('date',1)
	client.close()
	#return the template
	return render_to_response('yearStatistics.html', locals())


def prueba(request):
	#Código de mongodb
	client = MongoClient(ip, port)
	db = client['twitterdata']
	tweetCollection = db['tweets']
	for i in range(20):
		result2 = tweetCollection.map_reduce(mapCuentaDias, reduce,"myresult2", full_response = True)
		print result2	
	client.close()
	#return the template
	return render_to_response('userStatistics.html', locals())

mapRT = Code('function(){'
           'if (this.retweeted_status){'
           'emit(this.text, this.retweeted_status.retweet_count);'
           '}'
           '}')

reduceRT = Code("function (key, values) {"
               " var total = Math.max(values);"
               " return total;"
               "}")

mapUser = Code('function(){'
           '   emit(this.user.screen_name, 1);'
           '}')

mapPopular = Code('function(){'
           'var palabras = new Array;'
           'palabras = this.text.split(" ");'
           'for (var i = 0; i<palabras.length; i++){'
           '    var match = /^@/.test(palabras[i]);'
           '    if (match){'
           '        emit(palabras[i],1);'
           '    }'
           '}'
           '}')

mapHT = Code('function(){'
           'var palabras = new Array;'
           'palabras = this.text.split(" ");'
           'for (var i = 0; i<palabras.length; i++){'
           '    var match = /^#/.test(palabras[i]);'
           '    if (match){'
           '        emit(palabras[i],1);'
           '    }'
           '}'
           '}')

mapCuentaDias = Code('function(){'
           'var d = new Date();'
           'var mes = d.getMonth();'
           'var dia = d.getDay();'
           'var array = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];'
           'var arrayDias = [31,28,31,30,31,30,31,31,30,31,30,31];'
           'var filter = new RegExp(array[mes] + " ");'
           'var match = filter.test(this.created_at);'
           'if (match){'
           '    emit(this.created_at.split(" ")[1] + " " + this.created_at.split(" ")[2],1);'
           '}'
           'if (dia < 10){'
           '	dia = 10 - dia;'
           '	filter = new RegExp(array[mes-1] + " ");'
           '	match = filter.test(this.created_at);'
           '	if (match && arrayDias[mes-1]-dia<this.created_at.split(" ")[2]){'
           '    	emit(this.created_at.split(" ")[1] + " " + this.created_at.split(" ")[2],1);'
           '	}'

           '}'
           '}')

mapCuentaDiasRT = Code('function(){'
           'var d = new Date();'
           'var mes = d.getMonth();'
           'var dia = d.getDay();'
           'var array = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];'
           'var arrayDias = [31,28,31,30,31,30,31,31,30,31,30,31];'
           'var filter = new RegExp(array[mes] + " ");'
           'var match = filter.test(this.created_at);'
           'if (match && this.retweeted_status){'
           '    emit(this.created_at.split(" ")[1] + " " + this.created_at.split(" ")[2],1);'
           '}'
           'if (dia < 10){'
           '	dia = 10 - dia;'
           '	filter = new RegExp(array[mes-1] + " ");'
           '	match = filter.test(this.created_at);'
           '	if (match && arrayDias[mes-1]-dia<this.created_at.split(" ")[2] && this.retweeted_status){'
           '    	emit(this.created_at.split(" ")[1] + " " + this.created_at.split(" ")[2],1);'
           '	}'
           '}'
           '}')


mapCuentaMeses = Code('function(){'
           'var d = new Date();'
           'var mes = d.getMonth();'
           'var anio = d.getFullYear();'
           'var array = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];'
           'filter = new RegExp(anio);'
           'var match = filter.test(this.created_at);'
           'if (match){'
           '    emit(this.created_at.split(" ")[1]+ " " + this.created_at.split(" ")[5],1);'
           '}'
           'if (mes < 9){'
           '	mes = 11 - mes;'
           '	filter = new RegExp(array[mes-1] + " ");'
           '	match = filter.test(anio-1);'
           '	if (match && array.indexOf(this.created_at.split(" ")[2])>mes){'
           '    	emit(this.created_at.split(" ")[1] + " " + this.created_at.split(" ")[5],1);'
           '	}'
           '}'
           '}')

mapCuentaMesesRT = Code('function(){'
           'var d = new Date();'
           'var mes = d.getMonth();'
           'var anio = d.getFullYear();'
           'var array = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"];'
           'filter = new RegExp(anio);'
           'var match = filter.test(this.created_at);'
           'if (match && this.retweeted_status){'
           '    emit(this.created_at.split(" ")[1]+ " " + this.created_at.split(" ")[5],1);'
           '}'
           'if (mes < 9){'
           '	mes = 11 - mes;'
           '	filter = new RegExp(array[mes-1] + " ");'
           '	match = filter.test(anio-1);'
           '	if (match && array.indexOf(this.created_at.split(" ")[2])>mes && this.retweeted_status){'
           '    	emit(this.created_at.split(" ")[1] + " " + this.created_at.split(" ")[5],1);'
           '	}'
           '}'
           '}')
reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i];"
               "  }"
               "  return total;"
               "}")
