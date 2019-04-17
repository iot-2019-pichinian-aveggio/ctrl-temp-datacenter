#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <dht.h>

// Arduino Ethernet
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
byte ip[] = { 192, 168, 1, 101 };
//IPAddress gateway (192,168,1,1); //ip del gateway
//IPAddress subnet (255,255,255,0);

// Server / MQTT
char server[] = "www.google.com";    // name address for Google (using DNS)
char mqtt_server[] = "192.168.1.35";  // ip de raspberry pi
const char* clientID = "Client ID";
const char* mqtt_topic_temp = "temp";
const char* mqtt_topic_hum = "hum";
EthernetClient ethClient;
PubSubClient client(mqtt_server, 1883, ethClient);

// DHT
dht DHT;
#define DHT11_PIN 3

void setup()
{
  Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
  Serial.println("Antes de iniciar ethernet");
  iniciarEthernet(); //inicia una conexión ethernet
  Serial.println("Despues de iniciar ethernet");

  if (client.connect(clientID)) {
     Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  // mqtt temp
  int temp = DHT.temperature;
  char t[100];
  sprintf(t, "%d", temp);
  Serial.print("temperature ");
  Serial.println(t);
  if (client.publish(mqtt_topic_temp, t)) {
      Serial.println("Temp enviada!");
    }else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");        
      client.connect(clientID);
      delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
      client.publish(mqtt_topic_temp, t);         
    }
    delay(8000);

  // mqtt hum 
  int hum = DHT.humidity;
  char h[100];
  sprintf(h, "%d", hum);
  Serial.print("humidity ");
  Serial.println(h);
  if (client.publish(mqtt_topic_hum, h)) {
      Serial.println("Hum enviada!");
    }else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID);
      delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
      client.publish(mqtt_topic_hum, h);
    }
    delay(8000);
}

void iniciarEthernet(){  
  //Ethernet.begin(mac,ip,gateway,subnet); //si pudo conectar a internet manualmente
  Ethernet.begin(mac,ip); //si pudo conectar a internet manualmente
  Serial.println("conectando..."); 
  delay(1000); //Le da un segundo a Ethernet para que se inicialice   

  if (ethClient.connect(server, 80)) {
    Serial.println("connected");
    // Make a HTTP request:
    ethClient.println("GET /search?q=arduino HTTP/1.1");
    ethClient.println("Host: www.google.com");
    ethClient.println("Connection: close");
    ethClient.println();
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}
