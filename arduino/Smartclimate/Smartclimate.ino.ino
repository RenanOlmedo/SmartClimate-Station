#include <ESP8266WiFi.h>
#include <DHT.h>
#include <SFE_BMP180.h>
#include <Wire.h>

// ---- CONFIG Wi-Fi ----
#define STASSID "*****"
#define STAPSK  "*****"
const char* ssid = STASSID;
const char* pass = STAPSK;

const char* server = "api.thingspeak.com";  
String apiKey = "*******";  

WiFiClient client;

// ---- SENSOR DHT11 ----
#define DHTPIN D3      
#define DHTTYPE DHT11  
#define DHT_GND D5     // <<< GND do DHT controlado pelo ESP
DHT dht(DHTPIN, DHTTYPE);

float umidade = 0.0;
float temperaturaDHT = 0.0;

// ---- SENSOR BMP180 ----
SFE_BMP180 bmp;
#define ALTITUDE 708 // metros

char status;
double temperaturaBMP, pressao_abs, pressao_relativa;

// === Funções de sensores ===
void lerDHT() {
  umidade = dht.readHumidity();
  temperaturaDHT = dht.readTemperature();
}

void lerBMP() {
  status = bmp.startTemperature();
  if (status != 0) {
    delay(status);
    status = bmp.getTemperature(temperaturaBMP);
    if (status != 0) {
      status = bmp.startPressure(3);
      if (status != 0) {
        delay(status);
        status = bmp.getPressure(pressao_abs, temperaturaBMP);
        if (status != 0) {
          pressao_relativa = bmp.sealevel(pressao_abs, ALTITUDE);
        }
      }
    }
  }
}

// === Envio ao ThingSpeak ===
void enviarDados() {
  lerDHT();
  lerBMP();

  if (client.connect(server, 80)) {
    String postStr = apiKey;
    postStr += "&field1=" + String(umidade);
    postStr += "&field2=" + String(temperaturaDHT);
    postStr += "&field3=" + String(temperaturaBMP);
    postStr += "&field4=" + String(pressao_relativa);
    postStr += "&field5=" + String(pressao_abs);
    postStr += "\r\n\r\n";

    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(postStr.length());
    client.print("\n\n");
    client.print(postStr);

    Serial.println("=== Dados Enviados ===");
    Serial.print("Umidade (DHT11): "); Serial.println(umidade);
    Serial.print("Temp DHT11: "); Serial.print(temperaturaDHT); Serial.println(" °C");
    Serial.print("Temp BMP180: "); Serial.print(temperaturaBMP); Serial.println(" °C");
    Serial.print("Pressão Relativa: "); Serial.print(pressao_relativa); Serial.println(" hPa");
    Serial.print("Pressão Absoluta: "); Serial.print(pressao_abs); Serial.println(" hPa");
    Serial.println("======================");
  } else {
    Serial.println("Falha na conexão com ThingSpeak!");
  }
  client.stop();
}

// === SETUP ===
void setup() {
  Serial.begin(115200);

  // --- Liga o DHT pelo GND ---
  pinMode(DHT_GND, OUTPUT);
  digitalWrite(DHT_GND, LOW);   // GND ativo → DHT ligado
  delay(500);

  dht.begin();
  delay(2000);
  bmp.begin();
  delay(1000);

  Serial.println("Conectando ao WiFi...");
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  enviarDados();   // envia uma vez

  Serial.println("Desligando DHT e dormindo...");
  digitalWrite(DHT_GND, HIGH);   // <<< corta o GND → LED do módulo apaga

  delay(100);
  ESP.deepSleep(1800e6);   // 5 minutos
}

// === LOOP ===
void loop() {
  // nunca roda — ESP dorme
}
