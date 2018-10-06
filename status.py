#!/usr/bin/env python
#===========================================================================================
#init

import datetime
import time
import sys
import os
from PyQt4 import QtGui, QtCore
from twython import Twython

CONSUMER_KEY = 'vODk25RpPIMGkdwNG5aDTSHf7'
CONSUMER_SECRET = 'DDpHqywyPvEkUflnIaxyRCkQIW5GQodVUtZemaDwLUE1SY7mF3'
ACCESS_KEY = '929544340061478912-UwuRBEn4mWl4X8V5M7M7lk9Jlysc8xn'
ACCESS_SECRET = 'RTYlSugO6BUMHf6q1BLcmAgVOv4BrnJgV2z0Lgu559UwP'
TWEET = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

#===========================================================================================
#vars

POWER_LOSS = "no"

STATUS_INTERNET = "up"
STATUS_ROUTER = "up"
STATUS_GUNSAFE = "up"
STATUS_HVAC = "up"
STATUS_POWER = "up"

IP_INTERNET = "8.8.8.8"
IP_ROUTER = "192.168.1.1"
IP_HVAC = "192.168.1.250"
IP_GUNSAFE = "192.168.1.251"


#===========================================================================================
#functions

def CheckPing():
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
	s = str(t + "\t int:" + str(STATUS_INTERNET) + " rtr:" + str(STATUS_ROUTER) + " gunsafe:" + str(STATUS_GUNSAFE) + " hvac:" + str(STATUS_HVAC))
	print(s)

def CheckDown():
        global STATUS_INTERNET
	global STATUS_ROUTER
	global STATUS_GUNSAFE
	global STATUS_HVAC
	global POWER_LOSS

	t = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        if STATUS_GUNSAFE == "down":
                s = str(t + "\t ********** GUNSAFE NOT RESPONDING **********")
                Tweet(s)

        if STATUS_HVAC == "down":
                s = str(t + "\t ********** HVAC NOT RESPONDING **********")
                Tweet(s)

        if (STATUS_GUNSAFE == "down") and (STATUS_HVAC == "down") and (POWER_LOSS == "no"):
                s = str(t + "\t ********** AC POWER OFF **********")
                Tweet(s)
                s = str("ups1:dc ups2:dc ups3:dc dvr:halt cam1:up cam2:up cam3:up dellr710a:halt dellr710b:halt")
                Tweet(s)
                POWER_LOSS == "yes"

        if (STATUS_GUNSAFE == "down") and (STATUS_HVAC == "down") and (POWER_LOSS == "yes"):
                s = str(t + "\t ********** AC POWER OFF **********")
                Tweet(s)
                s = str("ups1:dc ups2:dc ups3:dc dvr:down cam1:down cam2:down cam3:down dellr710a:down dellr710b:down")
                Tweet(s)

        if ((STATUS_GUNSAFE == "up") or (STATUS_HVAC == "up")) and (POWER_LOSS == "yes"):
                s = str(t + "\t ********** AC POWER ON **********")
                Tweet(s)
                s = str("ups1:ac ups2:ac ups3:ac dvr:up cam1:up cam2:up cam3:up dellr710a:boot dellr710b:boot")
                Tweet(s)
                POWER_LOSS == "no"
                
                

def Tweet(s):
        try:
		TWEET.update_status(status = s)
		print(" ********** TWEET        **********")
	except:
		print(" ********** TWEET FAILED **********")


#===========================================================================================
#main

timer_check = QtCore.QTimer()
timer_check.timeout.connect(CheckPing())
timer_check.start(60000) #60s

timer_log = QtCore.QTimer()
timer_log.timeout.connect(Log())
timer_log.start(60000) #60s
	
timer_tweet = QtCore.QTimer()
timer_tweet.timeout.connect(CheckDown())
timer_tweet.start(300000) #5m
