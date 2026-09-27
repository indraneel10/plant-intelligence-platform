#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "CHANGE_ME";
const char* WIFI_PASSWORD = "CHANGE_ME";
const char* MQTT_HOST = "192.168.1.100";
const int MQTT_PORT = 1883;

const char* SENSOR_TOPIC = "plant/sensors";
const char* COMMAND_TOPIC = "plant/actuators/command";
const char* STATUS_TOPIC = "plant/actuators/status";

const int PUMP_PIN = 25;
const int VALVE_PINS[4] = {26, 27, 32, 33};
const int MAX_IRRIGATION_SECONDS = 60;
const unsigned long COMMAND_TIMEOUT_MS = 5000;

WiFiClient wifi;
PubSubClient mqtt(wifi);
unsigned long actionStartedAt = 0;
bool actionActive = false;
int activeValve = -1;

void allOff() {
  digitalWrite(PUMP_PIN, LOW);
  for (int i = 0; i < 4; i++) digitalWrite(VALVE_PINS[i], LOW);
  actionActive = false;
  activeValve = -1;
}

void publishStatus(const char* status) {
  StaticJsonDocument<256> doc;
  doc["status"] = status;
  doc["active"] = actionActive;
  doc["valve"] = activeValve;
  char buffer[256];
  serializeJson(doc, buffer);
  mqtt.publish(STATUS_TOPIC, buffer, true);
}

void executeCommand(JsonDocument& doc) {
  const char* action = doc["action_type"] | "";
  int zone = doc["zone_id"].as<String>().substring(5).toInt() - 1;
  int duration = doc["duration_seconds"] | 0;

  if (zone < 0 || zone >= 4 || duration <= 0 || duration > MAX_IRRIGATION_SECONDS) {
    allOff();
    publishStatus("REJECTED");
    return;
  }

  if (strcmp(action, "open_valve") != 0) {
    allOff();
    publishStatus("REJECTED");
    return;
  }

  allOff();
  digitalWrite(VALVE_PINS[zone], HIGH);
  digitalWrite(PUMP_PIN, HIGH);
  actionStartedAt = millis();
  actionActive = true;
  activeValve = zone;
  publishStatus("RUNNING");
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<512> doc;
  if (deserializeJson(doc, payload, length)) {
    allOff();
    publishStatus("INVALID_JSON");
    return;
  }
  executeCommand(doc);
}

void connectMqtt() {
  while (!mqtt.connected()) {
    if (mqtt.connect("esp32-wr04")) {
      mqtt.subscribe(COMMAND_TOPIC, 1);
      publishStatus("READY");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  pinMode(PUMP_PIN, OUTPUT);
  for (int i = 0; i < 4; i++) pinMode(VALVE_PINS[i], OUTPUT);
  allOff();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
}

void loop() {
  if (!mqtt.connected()) connectMqtt();
  mqtt.loop();

  if (actionActive && millis() - actionStartedAt >= (unsigned long)MAX_IRRIGATION_SECONDS * 1000UL) {
    allOff();
    publishStatus("TIMEOUT");
  }
}
