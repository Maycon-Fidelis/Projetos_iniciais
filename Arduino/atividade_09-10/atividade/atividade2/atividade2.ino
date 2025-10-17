/*
 * FreeRTOS no ESP32 – Demonstração de Mutex
 * --------------------------------------------
 * OBJETIVO:
 *  - Duas Tasks compartilham o mesmo recurso (Serial)
 *  - Um Mutex garante acesso exclusivo à Serial.println()
 *  - LED indica a Task de Alta Prioridade ativa.
 */

#include <Arduino.h>

// --- Definições ---
#define LED_PIN 2
#define TASK_STACK_SIZE 2048

// --- Handle do Mutex ---
SemaphoreHandle_t xSerialMutex;

// --- Protótipos ---
void vTaskHighPriority(void *pvParameters);
void vTaskLowPriority(void *pvParameters);

//================================================================
// 1. Task de Alta Prioridade (LED + Mensagens)
//================================================================
void vTaskHighPriority(void *pvParameters) {
  for (;;) {
    // Tenta pegar o Mutex (bloqueia até conseguir)
    if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {
      digitalWrite(LED_PIN, HIGH); // LED ON: Task de Alta prioridade ativa
      Serial.println("[HIGH] Acessando recurso Serial com prioridade alta...");
      vTaskDelay(pdMS_TO_TICKS(500)); // Simula tempo usando o recurso
      Serial.println("[HIGH] Saindo da seção crítica.\n");
      digitalWrite(LED_PIN, LOW);
      xSemaphoreGive(xSerialMutex); // Libera o Mutex
    }

    // Aguarda um pouco antes de tentar de novo
    vTaskDelay(pdMS_TO_TICKS(800));
  }
}

//================================================================
// 2. Task de Baixa Prioridade (mensagens periódicas)
//================================================================
void vTaskLowPriority(void *pvParameters) {
  for (;;) {
    if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {
      Serial.println("[LOW] Acessando recurso Serial com prioridade baixa...");
      vTaskDelay(pdMS_TO_TICKS(1000)); // Simula processamento lento
      Serial.println("[LOW] Saindo da seção crítica.\n");
      xSemaphoreGive(xSerialMutex);
    }

    vTaskDelay(pdMS_TO_TICKS(1200));
  }
}

//================================================================
// 3. Setup (Criação do Mutex e das Tasks)
//================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n--- FreeRTOS: Demonstração de MUTEX (Proteção de Recurso Serial) ---");

  pinMode(LED_PIN, OUTPUT);

  // Cria o Mutex (inicialmente “disponível”)
  xSerialMutex = xSemaphoreCreateMutex();
  if (xSerialMutex == NULL) {
    Serial.println("ERRO: Falha na criação do Mutex!");
    while (1);
  }

  // Cria as duas Tasks
  xTaskCreatePinnedToCore(
    vTaskHighPriority,
    "HighPriorityTask",
    TASK_STACK_SIZE,
    NULL,
    3,     // Prioridade mais alta
    NULL,
    1
  );

  xTaskCreatePinnedToCore(
    vTaskLowPriority,
    "LowPriorityTask",
    TASK_STACK_SIZE,
    NULL,
    1,     // Prioridade mais baixa
    NULL,
    1
  );

  Serial.println("Sistema inicializado. Observe as mensagens no Serial Monitor.");
}

//================================================================
// 4. Loop Principal (não usado)
//================================================================
void loop() {
  vTaskDelay(pdMS_TO_TICKS(5000));
}
