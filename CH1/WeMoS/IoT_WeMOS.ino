
#include "ThingSpeak.h"
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

//Replace your wifi credentials here
const char* ssid     = "TelstraBB9041";               // Replace with your Wifi Name
const char* password = "56m3n22k4d";                  // Replace with your wifi Password

//change your channel number here
unsigned long channel_num = 1264596;                  // Replace with your own ThingSpeak Account Channel ID (IoT)
const char * PrivateReadAPIKey = "884HMBXEZ0XP9RJ0";  // Read Channel Private Key

//channel fields.
int led;
unsigned int value;
WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(100);
  pinMode(D6, OUTPUT);
  digitalWrite(D6, 0);

  // We start by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");  
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Netmask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway: ");
  Serial.println(WiFi.gatewayIP());
  
  ThingSpeak.begin(client);          // connect the client to the thingSpeak server
}

void loop() {
 
  //get the last data of the fields
  led = ThingSpeak.readFloatField(channel_num, 1, PrivateReadAPIKey);    // read the last data of the field 1

  if(led == 1){
    digitalWrite(D6, 1);
    Serial.println("LED is On..!");
  }
  else if(led == 0){
    digitalWrite(D6, 0);
    Serial.println("LED is Off..!");
  }
  Serial.print("LED status:  ");
  Serial.println(led);
  client.flush();
  delay(1000);
}
