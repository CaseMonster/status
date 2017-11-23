#!/usr/bin/env python
#===========================================================================================
#init

import datetime
import time
import sys
import os
from PyQt4 import QtGui, QtCore
from twython import Twython

CONSUMER_KEY = 'bqDS6XtIuVHnFexDcS5nyMe4d'
CONSUMER_SECRET = 'pNcQyr2FEwJ7npMpNn58zwK8YRxnNncMVXvYxlpK2OkIEp6AVe'
ACCESS_KEY = '929546359300087809-dMQzlmgBoAMe9Iso5CY9kuinJKMa8xC'
ACCESS_SECRET = 'yoxbFZZQoGSDXMtjTCphXWf8D0vbcxHJ6RD0QNRNhI6gW'
TWEET = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

#===========================================================================================
#vars

STATUS_INTERNET = "up"
STATUS_ROUTER = "up"
STATUS_GUNSAFE = "up"
STATUS_HVAC = "up"

IP_INTERNET = "8.8.8.8"
IP_ROUTER = "192.168.1.1"
IP_GUNSAFE = "192.168.1.251"
IP_HVAC = "192.168.1.250"

#===========================================================================================
#functions

def Check():
	global STATUS_INTERNET
	global STATUS_ROUTER
	global STATUS_GUNSAFE
	global STATUS_HVAC
	global IP_INTERNET
	global IP_ROUTER
	global IP_GUNSAFE
	global IP_HVAC
	STATUS_INTERNET = Ping(IP_INTERNET)
	STATUS_ROUTER = Ping(IP_ROUTER)
	STATUS_GUNSAFE = Ping(IP_GUNSAFE)
	STATUS_HVAC = Ping(IP_HVAC)
	
def Ping(hostname):
	status = os.system("ping -c 1 " + hostname)
	if status == 0:
		return "up"
	else:
		return "down"

def Log():
	global STATUS_INTERNET
	global STATUS_ROUTER
	global STATUS_GUNSAFE
	global STATUS_HVAC
	t = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	s = str(t + "\t INTR: " + str(STATUS_INTERNET) + "\t ROTR: " + str(STATUS_ROUTER) + "\t GUNS: " + str(STATUS_GUNSAFE) + "\t HVAC: " + str(STATUS_HVAC))
	print(s)

def Tweet():
        global STATUS_INTERNET
	global STATUS_ROUTER
	global STATUS_GUNSAFE
	global STATUS_HVAC
	t = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	s = str(t + "\t INTR: " + str(STATUS_INTERNET) + "\t ROTR: " + str(STATUS_ROUTER) + "\t GUNS: " + str(STATUS_GUNSAFE) + "\t HVAC: " + str(STATUS_HVAC))
        try:
		TWEET.update_status(status = s)
		print(t + " ********** TWEET        **********")
	except:
		print(t + " ********** TWEET FAILED **********")

#===========================================================================================
#main

timer_check = QtCore.QTimer()
timer_check.timeout.connect(Check())
timer_check.start(60000) #60s

timer_log = QtCore.QTimer()
timer_log.timeout.connect(Log())
timer_log.start(60000) #60s
	
timer_tweet = QtCore.QTimer()
timer_tweet.timeout.connect(Tweet())
timer_tweet.start(300000) #5m
