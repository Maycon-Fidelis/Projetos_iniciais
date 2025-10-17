  /*
  * Código de Demonstração de Concorrência com FreeRTOS no ESP32.
  *
  * Duas tarefas independentes rodam simultaneamente:
  * 1. ledsTask: Pisca 3 LEDs em sequência.
  * 2. serialTask: Envia mensagens para o Monitor Serial.
  */

  // --Definição dos Pinos ---
      #define LED_1 13 // LED 1: Geralmente o LED Onboard
      #define LED_2 12 // LED 2
      #define LED_3 22 // LED 3

  // --Handles de Tarefas (Para controle futuro, se necessário) ---
      TaskHandle_t ledTask1Handle = NULL;
      TaskHandle_t ledTask2Handle = NULL;
      TaskHandle_t ledTask3Handle = NULL;

      TaskHandle_t serialTaskHandle = NULL;

  //================================================================
  // 1. Task dos LEDs (Responsável por piscar os 3 LEDs)
  //================================================================

  void ledsTask1(void *pvParameters) {
  // Inicializa os pinos como saída
  pinMode(LED_1, OUTPUT);

  // Loop principal da tarefa Roda eternamente
      for (;;) {

      // --Ciclo de Pisca-Pisca Sequencial ---

      // LED 1
      digitalWrite(LED_1, HIGH);
      vTaskDelay(1000 / portTICK_PERIOD_MS); // Bloqueia e libera a CPU
      digitalWrite(LED_1, LOW);
      vTaskDelay(1000 / portTICK_PERIOD_MS);
      // Espera antes de reiniciar o ciclo
      //vTaskDelay(400 / portTICK_PERIOD_MS);
      }
    }

    void ledsTask2(void *pvParameters) {
      pinMode(LED_2,OUTPUT);

      for (;;) {
        digitalWrite(LED_2, HIGH);
        vTaskDelay(2000 / portTICK_PERIOD_MS); // Bloqueia e libera a CPU
        digitalWrite(LED_2, LOW);
        vTaskDelay(2000 / portTICK_PERIOD_MS);
      }
    }

    void ledsTask3(void *pvParameters) {
      pinMode(LED_3,OUTPUT);

      for (;;) {
        digitalWrite(LED_3, HIGH);
        vTaskDelay(3000 / portTICK_PERIOD_MS); // Bloqueia e libera a CPU
        digitalWrite(LED_3, LOW);
        vTaskDelay(3000 / portTICK_PERIOD_MS);
      }
      
    }

  //================================================================
  // 2. Task Serial (Responsável por enviar o "oi")
  //================================================================

  void serialTask(void *pvParameters) {
  // Loop principal da tarefa Roda eternamente
      for (;;) {
      // Imprime a mensagem.
      Serial.println("--Olá, Serial! Esta mensagem é enviada CONCORRENTEMENTE com os LEDs! ---");

      // Bloqueia a tarefa por 1.5 segundos, liberando a CPU para outras Tasks.
      vTaskDelay(100 / portTICK_PERIOD_MS);
      }
  }

  //================================================================
  // 3. Configuração (setup)
  //================================================================

  void setup() {
  Serial.begin(115200);
  delay(1000); // Espera o serial iniciar
  Serial.println("\n--Configuração FreeRTOS Iniciada ---");

  // 1. Cria a Tarefa dos LEDs
  // xTaskCreate(Função, Nome, Pilha, Parâmetros, Prioridade, Handle)
  xTaskCreate(
    ledsTask1,
    "LED1_Task",
    1024,
    NULL,
    1, // Prioridade
    &ledTask1Handle
  );

  xTaskCreate(
    ledsTask2,
    "LED2_Task",
    1024,
    NULL,
    1, // mesma prioridade (ou ajuste se quiser diferente)
    &ledTask2Handle
  );

  xTaskCreate(
    ledsTask3,
    "LED3_Task",
    1024,
    NULL,
    1, // mesma prioridade
    &ledTask3Handle
  );


  // 2. Cria a Tarefa Serial
  xTaskCreate(
  serialTask,
  "Serial_Task",
  2048, // Pilha maior para funções de I/O
  NULL,
  2, // Prioridade Média (ligeiramente maior que a do LED)
  &serialTaskHandle
  );

  Serial.println("Ambas as tarefas foram criadas e estão sendo gerenciadas pelo FreeRTOS!");
  }

  //================================================================
  // 4. Loop Principal (Não utilizado, mas necessário)
  //================================================================

  void loop() {
  // O scheduler do FreeRTOS assume o controle no setup.
  // Esta função pode ficar vazia, pois as tarefas rodam de forma independente.
  }