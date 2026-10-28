
/*
  Real-Time Voice-Based Alert Classification Using Python and Arduino

  HIGH priority LED:   D8
  MEDIUM priority LED: D9
  LOW priority LED:   D10
  Optional buzzer:    D11

  Serial commands at 9600 baud:
  H = HIGH priority
  M = MEDIUM priority
  L = LOW priority
  Q = switch all LEDs off
*/

const byte HIGH_LED_PIN = 8;
const byte MEDIUM_LED_PIN = 9;
const byte LOW_LED_PIN = 10;
const byte BUZZER_PIN = 11;

const bool USE_BUZZER = false;


void allOff() {
  digitalWrite(HIGH_LED_PIN, LOW);
  digitalWrite(MEDIUM_LED_PIN, LOW);
  digitalWrite(LOW_LED_PIN, LOW);

  if (USE_BUZZER) {
    noTone(BUZZER_PIN);
    digitalWrite(BUZZER_PIN, LOW);
  }
}


void signalPriority(char command) {
  allOff();

  switch (command) {
    case 'H':
      digitalWrite(HIGH_LED_PIN, HIGH);

      if (USE_BUZZER) {
        tone(BUZZER_PIN, 1800, 500);
      }

      Serial.println("ACK:HIGH");
      break;

    case 'M':
      digitalWrite(MEDIUM_LED_PIN, HIGH);
      Serial.println("ACK:MEDIUM");
      break;

    case 'L':
      digitalWrite(LOW_LED_PIN, HIGH);
      Serial.println("ACK:LOW");
      break;

    case 'Q':
      Serial.println("ACK:OFF");
      break;

    default:
      Serial.print("ERR:UNKNOWN_COMMAND:");
      Serial.println(command);
      break;
  }
}


void setup() {
  pinMode(HIGH_LED_PIN, OUTPUT);
  pinMode(MEDIUM_LED_PIN, OUTPUT);
  pinMode(LOW_LED_PIN, OUTPUT);

  if (USE_BUZZER) {
    pinMode(BUZZER_PIN, OUTPUT);
  }

  allOff();

  Serial.begin(9600);

  Serial.println("Voice-Based Alert Classification System ready");
}


void loop() {
  while (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '\n' || command == '\r' || command == ' ') {
      continue;
    }

    signalPriority(command);
  }
}
