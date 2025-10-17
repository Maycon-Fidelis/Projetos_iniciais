const int led = 15;
const int botao = 2;
const int lampada = 14;

bool ledStatus = false;

void setup(){
  pinMode(botao, INPUT_PULLUP);
  pinMode(led, OUTPUT);
  pinMode(lampada, OUTPUT);
  digitalWrite(led, HIGH);
  digitalWrite(lampada, HIGH);
  Serial.begin(115200);
}

void loop(){
  if (digitalRead(botao) == LOW){
    delay(50); // debounce simples

    while(digitalRead(botao) == LOW) {} // espera soltar o botão

    ledStatus = !ledStatus;

    digitalWrite(led, ledStatus ? LOW : HIGH);
    digitalWrite(lampada, ledStatus ? LOW : HIGH);

    delay(50); // debounce após soltar
  }
}