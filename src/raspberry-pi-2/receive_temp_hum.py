# MQTT
import paho.mqtt.client as mqtt 
MQTT_SERVER = "localhost"
MQTT_PATH_TEMP = "temp"
MQTT_PATH_HUM = "hum"
 

# FIREBASE
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

PAHT_CRED = './cred.json'
URL_DB = 'https://iot-proyecto1.firebaseio.com/'
REF_HOME = 'home'
# data
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


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
 
	# Subscribing in on_connect() means that if we lose the connection and
  	# reconnect then subscriptions will be renewed.
  	client.subscribe(MQTT_PATH_TEMP)
  	client.subscribe(MQTT_PATH_HUM)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    	print(msg.topic+" "+str(msg.payload))
	if (msg.topic == "temp"):
		setTemperature(str(msg.payload))
	elif (msg.topic == "hum"):
		setHumidity(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

# FIREBASE
def initDB():
	refData.set({
		'humidity': 10,
	       	'temperature': 0
	})	
	print('Ok estructuraInicialDB!')

def setTemperature(t):		
	refTemp.set(t)
	refStateTemp1.set(t)
	print(' set Temperature in '+t)

def setHumidity(h):			
	refHum.set(h)
	print(' set Humidity in '+h)		

cred = credentials.Certificate(PAHT_CRED)
firebase_admin.initialize_app(cred, {
	'databaseURL': URL_DB
})

# HOME
refHome = db.reference(REF_HOME)	
# DATA
refData = refHome.child(REF_DATA)	
refTemp = refData.child(REF_TEMPERATURE)	
refHum = refData.child(REF_HUMIDITY)	
#CONTROL
refControl = refHome.child(REF_CONTROL)
#AIR 1
refAir1 = refControl.child(REF_AIR1)
refConfiguration1 = refAir1.child(REF_CONFIGURATION)
refConfChange1 = refConfiguration1.child(REF_CONF_CHANGE)
refConfOn1 = refConfiguration1.child(REF_CONF_ON)
refConfTempMax1 = refConfiguration1.child(REF_CONF_TEMPERATUREMAX)
refConfTempMin1 = refConfiguration1.child(REF_CONF_TEMPERATUREMIN)
		
refState1 = refAir1.child(REF_STATE)			
refStateOn1 = refState1.child(REF_STATE_ON)
refStateTemp1 = refState1.child(REF_STATE_TEMPERATURE)
		

initDB()
client.loop_forever()
