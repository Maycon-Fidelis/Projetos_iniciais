/*
 * Sincronização ISR (Interrupção) -> Task (FreeRTOS no ESP32)
 * -----------------------------------------------------------------
 * OBJETIVO: Usar um Semáforo Binário para que o pressionar de um botão
 * (detectado pela ISR) acorde imediatamente uma Task que está dormindo,
 * esperando pelo evento.
 * * HARDWARE:
 * - Botão: Conectado entre o Pino 13 e o GND (o PULLUP interno do ESP32 é usado).
 * - LED: O LED on-board no Pino 2 será usado como feedback.
 */

// As bibliotecas FreeRTOS são incluídas automaticamente ao compilar para ESP32.
// Apenas o Arduino.h é necessário para as funções básicas.
#include <Arduino.h>

// --- Definições ---
#define BUTTON_PIN      13         // Pino para o botão (com interrupção)
#define LED_PIN         2          // LED de feedback (Geralmente o LED on-board)
#define TASK_STACK_SIZE 2048       // Tamanho da pilha para a Task

// --- Handle do Semáforo ---
// O Handle é a "referência" ao nosso semáforo binário.
SemaphoreHandle_t xButtonSemaphore = NULL;

// --- Protótipos das Funções ---
void vTaskButtonProcessor(void *pvParameters);
void IRAM_ATTR isrButtonHandler();


//================================================================
// 1. Rotina de Serviço de Interrupção (ISR)
//================================================================
// A macro IRAM_ATTR é fundamental no ESP32 para garantir que esta rotina
// rode a partir da RAM interna, o que é crucial para performance.

void IRAM_ATTR isrButtonHandler() {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
   
    // Libera (GIVE) o Semáforo, sinalizando que o evento ocorreu.
    // **xSemaphoreGiveFromISR** é a função segura para ISRs.
    xSemaphoreGiveFromISR(xButtonSemaphore, &xHigherPriorityTaskWoken);
   
    // Se a Task que estava esperando por este semáforo tinha uma prioridade
    // maior do que a Task que estava rodando, forçamos a troca de contexto.
    if (xHigherPriorityTaskWoken == pdTRUE) {
        portYIELD_FROM_ISR(); // Força o escalonador a rodar a Task de maior prioridade.
    }
}

//================================================================
// 2. Task de Processamento de Eventos
//================================================================
// Esta Task é responsável por lidar com o evento do botão de forma assíncrona.

void vTaskButtonProcessor(void *pvParameters) {
    Serial.println(">>> Task de Processamento: Pronta e esperando pelo botão...");
   
    for (;;) {
        // Tenta pegar (TAKE) o Semáforo.
        // A Task BLOQUEIA AQUI, entregando o controle da CPU, até que a ISR libere o semáforo.
        if (xSemaphoreTake(xButtonSemaphore, portMAX_DELAY) == pdTRUE) {
           
            // --- REGIÃO DE PROCESSAMENTO (SÓ RODA APÓS O BOTÃO) ---
           
            Serial.print("\n[EVENTO RECEBIDO]");
            Serial.println(" Processando dados do botão.");
           
            // Simulação de alguma lógica/feedback
            digitalWrite(LED_PIN, HIGH);
            vTaskDelay(pdMS_TO_TICKS(100)); // Pequeno atraso (100ms)
            digitalWrite(LED_PIN, LOW);
           
            Serial.println("[EVENTO CONCLUÍDO] Task voltando a bloquear e esperar...");
            // O loop volta ao topo e a Task bloqueia novamente no xSemaphoreTake().
        }
    }
}

//================================================================
// 3. Configuração (setup)
//================================================================

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n--- FreeRTOS: Exemplo de Sincronização ISR <--> Task ---");

    // Configuração do Hardware
    pinMode(LED_PIN, OUTPUT);
    // Configura o pino do botão com PULLUP interno, o botão deve ir para GND.
    pinMode(BUTTON_PIN, INPUT_PULLUP);

    // 1. Criação do Semáforo Binário
    // É criado "vazio" (0), então a Task começará bloqueada.
    xButtonSemaphore = xSemaphoreCreateBinary();
   
    if (xButtonSemaphore == NULL) {
        Serial.println("ERRO: Falha crítica na criação do Semáforo.");
        while(1); // Para o programa se o recurso falhar.
    }

    // 2. Anexa a Interrupção
    // Chama a isrButtonHandler na borda de descida (FALLING) - LOW quando o botão é pressionado.
    attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), isrButtonHandler, FALLING);

    // 3. Criação da Task de Processamento
    xTaskCreatePinnedToCore(
        vTaskButtonProcessor,
        "Button_Proc_Task",
        TASK_STACK_SIZE,
        NULL,
        2, // Prioridade Média (Maior que o loop() e menor que Tasks muito críticas)
        NULL,
        1  // Core 1 (App_CPU)
    );

    Serial.println("Sistema inicializado. Pressione o botão para disparar o evento.");
}

//================================================================
// 4. Loop Principal (Não utilizado no gerenciamento RTOS)
//================================================================

void loop() {
    // A Task loop() tem a prioridade mais baixa.
    // Ela só rodará se a vTaskButtonProcessor estiver bloqueada (que é o que queremos).
    // Podemos deixar o loop vazio ou usar para tarefas de manutenção de prioridade baixíssima.
    vTaskDelay(pdMS_TO_TICKS(5000)); // Atraso longo apenas para ceder a CPU de volta
}