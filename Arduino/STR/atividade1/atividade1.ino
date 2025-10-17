// Defina o pino do LED
#define LED_PIN1 13
#define LED_PIN2 12
#define LED_PIN3 22

// Handle para a tarefa
TaskHandle_t ledTaskHandle = NULL;

// Função da tarefa que pisca o LED
void ledTask(void *pvParameters) {
   pinMode(LED_PIN1, OUTPUT);
   pinMode(LED_PIN2, OUTPUT);
   pinMode(LED_PIN3, OUTPUT);

   Serial.println(">>> Tarefa LEDs: Iniciada e controlando as luzes.");

   for (;;) {
   digitalWrite(LED_PIN1, HIGH);
   vTaskDelay(1000 / portTICK_PERIOD_MS); // Espera 1 segundo
   digitalWrite(LED_PIN1, LOW);
   vTaskDelay(1000 / portTICK_PERIOD_MS); // Espera 1 segundo
   digitalWrite(LED_PIN2, HIGH);
   vTaskDelay(1000 / portTICK_PERIOD_MS); // Espera 1 segundo
   digitalWrite(LED_PIN2, LOW);
   vTaskDelay(1000 / portTICK_PERIOD_MS); // Espera 1 segundo
   digitalWrite(LED_PIN3, HIGH);
   vTaskDelay(1000 / portTICK_PERIOD_MS); // Espera 1 segundo
   digitalWrite(LED_PIN3, LOW);
   vTaskDelay(1000 / portTICK_PERIOD_MS); // Espera 1 segundo
   Serial.println("Oi");
   }
}

// Função de configuração (setup)
void setup() {
Serial.begin(115200);
   // Crie a tarefa para o LED
   xTaskCreate(
   ledTask, // A função da tarefa
   "LED_Blink", // Nome da tarefa para depuração
   1024, // Tamanho da pilha (em bytes)
   NULL, // Parâmetro passado para a tarefa
   1, // Prioridade da tarefa (quanto maior, mais prioridade)
   &ledTaskHandle // Handle da tarefa
   );
}

// A função loop do Arduino não será usada neste exemplo
void loop() {
// A tarefa já está rodando
}
