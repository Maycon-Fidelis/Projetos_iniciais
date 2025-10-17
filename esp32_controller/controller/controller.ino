#include <WiFi.h>
#include <HTTPClient.h>

// 🔹 Configurações de rede
const char* ssid = "DTEL_MAYCON";
const char* password = "88942839";

// 🔹 Servidor destino
const char* serverUrl = "http://192.168.0.105:3000/medicao";

// 🔹 Estrutura para armazenar as medições
struct SensorData {
  float ph;
  float temperatura;
  float turbidez;
  String data;
  String horario;
  int subareaId;
};

// 🔹 Variável global protegida (com Mutex)
SensorData sensorData;
SemaphoreHandle_t xMutex;

// 🔹 Protótipos das tasks
void TaskLeitura(void *pvParameters);
void TaskEnvio(void *pvParameters);

void setup() {
  Serial.begin(115200);

  // Conecta ao Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Conectando ao Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n✅ Wi-Fi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());

  // Cria Mutex
  xMutex = xSemaphoreCreateMutex();

  // Cria as duas tasks do FreeRTOS
  xTaskCreatePinnedToCore(TaskLeitura, "LeituraSensores", 4096, NULL, 1, NULL, 1);
  xTaskCreatePinnedToCore(TaskEnvio, "EnvioServidor", 8192, NULL, 1, NULL, 1);
}

void loop() {
  // Nada aqui! FreeRTOS gerencia as tasks.
}

void TaskLeitura(void *pvParameters) {
  for (;;) {
    // Gera dados simulados (como se fossem sensores)
    float ph = random(60, 80) / 10.0;
    float temperatura = random(200, 320) / 10.0;
    float turbidez = random(10, 100) / 10.0;

    // Atualiza dados globais com Mutex
    if (xSemaphoreTake(xMutex, (TickType_t)10) == pdTRUE) {
      sensorData.ph = ph;
      sensorData.temperatura = temperatura;
      sensorData.turbidez = turbidez;
      sensorData.data = "2025-10-08";
      sensorData.horario = "12:00";
      sensorData.subareaId = 1;
      xSemaphoreGive(xMutex);
    }

    Serial.printf("[Leitura] PH: %.1f | Temp: %.1f | Turbidez: %.1f\n", ph, temperatura, turbidez);
    vTaskDelay(pdMS_TO_TICKS(3000)); // lê a cada 3s
  }
}

void TaskEnvio(void *pvParameters) {
  for (;;) {
    if (WiFi.status() == WL_CONNECTED) {
      SensorData copia;

      // Copia dados com segurança
      if (xSemaphoreTake(xMutex, (TickType_t)10) == pdTRUE) {
        copia = sensorData;
        xSemaphoreGive(xMutex);
      }

      // Monta JSON
      String json = "{";
      json += "\"data\":\"" + copia.data + "\",";
      json += "\"horario\":\"" + copia.horario + "\",";
      json += "\"subareaId\":" + String(copia.subareaId) + ",";
      json += "\"ph\":" + String(copia.ph, 1) + ",";
      json += "\"temperatura\":" + String(copia.temperatura, 1) + ",";
      json += "\"turbidez\":" + String(copia.turbidez, 1);
      json += "}";

      Serial.println("\n[Envio] Enviando JSON:");
      Serial.println(json);

      HTTPClient http;
      http.begin(serverUrl);
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST(json);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("[Envio] Resposta do servidor:");
        Serial.println(response);
      } else {
        Serial.printf("[Envio] Erro HTTP: %d\n", httpResponseCode);
      }

      http.end();
    } else {
      Serial.println("[Envio] Wi-Fi desconectado! Tentando reconectar...");
      WiFi.reconnect();
    }

    vTaskDelay(pdMS_TO_TICKS(5000)); // Envia a cada 5s
  }
}
