#!/usr/bin/python
# -*- coding: utf-8 -*-
# autor: German
# Abril de 2018

import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# MQTT
MQTT_SERVER = "localhost"
MQTT_TOPIC_AIR1 = "air1"

# Firebase
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread

PAHT_CRED = './cred.json'
URL_DB = 'https://iot-proyecto1.firebaseio.com/'
REF_HOME = 'home'

REF_DATA = 'data'
REF_TEMPERATURE = 'temperature'
REF_HUMIDITY = 'humidity'

REF_CONTROL = 'control'
REF_AIR1 = 'air1'
# configuration
REF_CONFIGURATION = 'configuration'
REF_CONF_CHANGE = 'change'
REF_CONF_ON = 'on'
REF_CONF_TEMPERATUREMAX = 'temperatureMaxIn'
REF_CONF_TEMPERATUREMIN = 'temperatureMinIn'
# state
REF_STATE = 'state'
REF_STATE_ON = 'on'
REF_STATE_TEMPERATURE = 'temperature'

REF_AIR2 = 'air2'

REF_MESSAGE = 'message'
REF_ERROR = 'error'
REF_OK = 'ok'

class IOT():	
	confAir1On = True
	confAir1TempMax = "0"
	confAir1TemMin = "0"

	stateAir1On = True
	stateAir1Temp =	"0"

	def __init__(self):
	        cred = credentials.Certificate(PAHT_CRED)
            	firebase_admin.initialize_app(cred, {
                	'databaseURL': URL_DB
		})

		#HOME
	   	self.refHome = db.reference(REF_HOME)	
		#DATA
		self.refData = self.refHome.child(REF_DATA)	
		self.refTemp = self.refData.child(REF_TEMPERATURE)	
		self.refHum = self.refData.child(REF_HUMIDITY)	
		#CONTROL
		self.refControl = self.refHome.child(REF_CONTROL)

		#AIR 1
		self.refAir1 = self.refControl.child(REF_AIR1)
		self.refConfiguration1 = self.refAir1.child(REF_CONFIGURATION)
		self.refConfChange1 = self.refConfiguration1.child(REF_CONF_CHANGE)
		self.refConfOn1 = self.refConfiguration1.child(REF_CONF_ON)
		self.refConfTempMax1 = self.refConfiguration1.child(REF_CONF_TEMPERATUREMAX)
		self.refConfTempMin1 = self.refConfiguration1.child(REF_CONF_TEMPERATUREMIN)
		
		self.refState1 = self.refAir1.child(REF_STATE)			
		self.refStateOn1 = self.refState1.child(REF_STATE_ON)
		self.refStateTemp1 = self.refState1.child(REF_STATE_TEMPERATURE)
			
		#MESSAGE
		self.refMessage = self.refHome.child(REF_MESSAGE)	
		self.refError = self.refMessage.child(REF_ERROR)
		self.refOk = self.refMessage.child(REF_OK)
			
	    	self.initDB() # solo ejecutar la primera vez		
	    	self.initConfigurationAir1() 
	    	self.initStateAir1() 
	    	print ('Ok init!')
	
	def initDB(self):
        	self.refData.set({
			'humidity': 0,
	       		'temperature': 0
		})	
		print('Ok estructuraInicialDB!')

	def initConfigurationAir1(self):
		IOT.confAir1On = self.refConfOn1.get()
		IOT.confAir1TempMax = self.refConfTempMax1.get()
		IOT.confAir1TempMin = self.refConfTempMin1.get()
		print 'change detected - initConfigurationAir1'

	def initStateAir1(self):
		IOT.stateAir1On = self.refStateOn1.get()
		IOT.stateAir1Temp = self.refStateTemp1.get()

	def setChangeAir1ToFalse(self, v):
		self.refConfChange1.set(v)
		print(self.refOk.get() + ' set Pending1 in '+str(v))	

	def checkConfiguration1(self):
		while True:
			varPending = self.refConfChange1.get()
			if varPending == True:								
				self.initConfigurationAir1()
				self.setChangeAir1ToFalse(False)
	
			time.sleep(6)

	def sendSignalAir1On(self, v):
		if (v):
			publish.single(MQTT_TOPIC_AIR1, "on", hostname=MQTT_SERVER)
		else:
			publish.single(MQTT_TOPIC_AIR1, "off", hostname=MQTT_SERVER)

	def setStateAir1On(self, v):
		self.refStateOn1.set(v)

	def controlAir1(self):		
		while (True):
			print 'A'
			if (IOT.confAir1On == True): # Si el aire está ON
				print 'B'
				varTemp = self.refTemp.get()	# Obtengo temp
				# Si está entre los valores definidos
				print varTemp
				print int(IOT.confAir1TempMax)
				print int(IOT.confAir1TempMin)
				if ((int(varTemp) < int(IOT.confAir1TempMax)) and (int(varTemp) > int(IOT.confAir1TempMin))):
					print 'C'
					if (IOT.stateAir1On == True):	# Si el estado está definido en ON
						print 'D'
						self.sendSignalAir1On(False)	# Apagar aire						
						self.setStateAir1On(False)	# Setear en base el estado						
				elif (IOT.stateAir1On == False):
					print 'E'
					self.sendSignalAir1On(True)
					self.setStateAir1On(True)
			elif (IOT.stateAir1On == True):
				print 'F'
				self.sendSignalAir1On(False)
				self.setStateAir1On(False)
			
			self.initStateAir1()
			print 'antes de sleep'
			time.sleep(4)

	
	
# START
print ('START !')
iot = IOT()

subprocess_configuration1 = Thread(target=iot.checkConfiguration1)
subprocess_configuration1.deamon = True
subprocess_configuration1.start()

subprocess_control1 = Thread(target=iot.controlAir1)
subprocess_control1.deamon = True
subprocess_control1.start()

