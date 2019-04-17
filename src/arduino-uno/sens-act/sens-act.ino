#include <SoftwareSerial.h>
#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <dht.h>

// Arduino Ethernet
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
byte ip[] = { 192, 168, 1, 101 };
//IPAddress gateway (192,168,1,1); //ip del gateway
//IPAddress subnet (255,255,255,0);
