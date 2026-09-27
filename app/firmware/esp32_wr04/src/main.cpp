#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
const char* WIFI_SSID="CHANGE_ME"; const char* WIFI_PASSWORD="CHANGE_ME"; WebServer server(80);
const int ZONE_PINS[]={25,26,27,32}; const char* ZONE_IDS[]={"zone-1","zone-2","zone-3","zone-4"}; const size_t ZONE_COUNT=4; const uint32_t MAX_DURATION_SECONDS=300;
void allOff(){for(size_t i=0;i<ZONE_COUNT;i++)digitalWrite(ZONE_PINS[i],LOW);} int zoneIndex(const String&id){for(size_t i=0;i<ZONE_COUNT;i++)if(id==ZONE_IDS[i])return i;return -1;}
void irrigation(){StaticJsonDocument<256> doc; if(deserializeJson(doc,server.arg("plain"))){server.send(400,"application/json","{\"error\":\"invalid_json\"}");return;} String action=doc["action_type"]|"";String zone=doc["zone_id"]|"";uint32_t duration=doc["duration_seconds"]|0;int idx=zoneIndex(zone);if(action!="water"||idx<0||duration==0||duration>MAX_DURATION_SECONDS){allOff();server.send(422,"application/json","{\"error\":\"invalid_action\"}");return;} allOff();digitalWrite(ZONE_PINS[idx],HIGH);delay(duration*1000UL);digitalWrite(ZONE_PINS[idx],LOW);server.send(200,"application/json",String("{\"status\":\"accepted\",\"zone_id\":\"")+zone+"\",\"duration_seconds\":"+duration+"}");}
void setup(){for(size_t i=0;i<ZONE_COUNT;i++){pinMode(ZONE_PINS[i],OUTPUT);digitalWrite(ZONE_PINS[i],LOW);}WiFi.begin(WIFI_SSID,WIFI_PASSWORD);while(WiFi.status()!=WL_CONNECTED)delay(250);server.on("/v1/actuators/irrigation",HTTP_POST,irrigation);server.begin();} void loop(){server.handleClient();}
