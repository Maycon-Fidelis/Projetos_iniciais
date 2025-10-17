#include <Arduino.h>

// --- Definições ---
#define BUTTON_PIN      13
#define LED1_PIN        1
#define LED2_PIN        22
#define LED3_PIN        23
#define TASK_STACK_SIZE 2048

SemaphoreHandle_t xButtonSemaphore = NULL;

// --- Protótipos ---
void vTaskButtonProcessor(void *pvParameters);
void IRAM_ATTR isrButtonHandler();

// --- Variável global de estado ---
volatile int currentLED = 0;

//================================================================
// ISR - Interrupção do botão
//================================================================
void IRAM_ATTR isrButtonHandler() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  xSemaphoreGiveFromISR(xButtonSemaphore, &xHigherPriorityTaskWoken);
  if (xHigherPriorityTaskWoken == pdTRUE) {
    portYIELD_FROM_ISR();
  }
}

//================================================================
// Task de processamento do evento
//================================================================
void vTaskButtonProcessor(void *pvParameters) {
  Serial.println(">>> Task aguardando o botão...");

  for (;;) {
    if (xSemaphoreTake(xButtonSemaphore, portMAX_DELAY) == pdTRUE) {
      Serial.println("\n[EVENTO RECEBIDO] Trocar LED.");

      // Desliga todos os LEDs
      digitalWrite(LED1_PIN, LOW);
      digitalWrite(LED2_PIN, LOW);
      digitalWrite(LED3_PIN, LOW);

      // Avança para o próximo LED
      currentLED++;
      if (currentLED > 3) currentLED = 1;

      // Liga o LED correspondente
      switch (currentLED) {
        case 1: digitalWrite(LED1_PIN, HIGH); break;
        case 2: digitalWrite(LED2_PIN, HIGH); break;
        case 3: digitalWrite(LED3_PIN, HIGH); break;
      }

      Serial.print("LED atual: ");
      Serial.println(currentLED);

      vTaskDelay(pdMS_TO_TICKS(200)); // anti-repique simples
    }
  }
}

//================================================================
// Setup
//================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n--- FreeRTOS: ISR + Semáforo + Múltiplos LEDs ---");

  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Cria o semáforo
  xButtonSemaphore = xSemaphoreCreateBinary();
  if (xButtonSemaphore == NULL) {
    Serial.println("ERRO: falha ao criar semáforo!");
    while (1);
  }

  // Anexa interrupção
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), isrButtonHandler, FALLING);

  // Cria a Task
  xTaskCreatePinnedToCore(
    vTaskButtonProcessor,
    "ButtonTask",
    TASK_STACK_SIZE,
    NULL,
    2,
    NULL,
    1
  );

  Serial.println("Sistema pronto! Pressione o botão.");
}

void loop() {
  vTaskDelay(pdMS_TO_TICKS(5000));
}
