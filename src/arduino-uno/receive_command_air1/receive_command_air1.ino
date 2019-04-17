#include <SoftwareSerial.h>
#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// leds
int ledAirOn = 7;
int ledAirOff = 4;

// Update these with values suitable for your network.
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 100);
IPAddress server(192, 168, 1, 35);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String command = "on";
  
  for (int i=0;i<length;i++) {
    command += (char)payload[i];
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println(command); 

  if (command == "on"){
    Serial.println("in"); 
    digitalWrite(ledAirOn,HIGH);
    digitalWrite(ledAirOff, LOW);
    delay(2000);
  }else{
    Serial.println("out");
    digitalWrite(ledAirOff, HIGH);
    digitalWrite(ledAirOn,LOW);
    delay(2000);
  }
}

// MQTT
EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);
const char* clientID = "Client ID";
const char* mqtt_topic_air1 = "air1";

void setup()
{
  Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
  pinMode(ledAirOff, OUTPUT); //LED 4 como salida
  pinMode(ledAirOn, OUTPUT); //LED 7 como salida
  Serial.println("A");
  Ethernet.begin(mac, ip);
  
  if (client.connect(clientID)) {
    Serial.println("B");
    client.subscribe(mqtt_topic_air1);
  }  
}



void loop()
{
  client.loop(); 
}
