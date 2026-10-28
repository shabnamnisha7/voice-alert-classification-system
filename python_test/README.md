
# Real-Time Voice-Based Alert Classification Using Python and Arduino

A prototype that listens for spoken public announcements, assigns a rule-based
priority, signals an Arduino Uno using LEDs, records recognized announcements
to CSV, and displays the history in a Streamlit dashboard.

## Project structure

- `arduino/AIoT_Public_Alert_Gateway.ino`: Arduino LED controller
- `python_test/control.py`: microphone, speech recognition, logging and serial communication
- `python_test/classifier.py`: English keyword-based priority classification
- `python_test/test_classifier.py`: automated classification tests
- `python_test/dashboard.py`: Streamlit dashboard
- `python_test/requirements.txt`: Python dependencies
- `python_test/alert_history.csv`: generated automatically after the first logged alert

## Hardware wiring

Use an Arduino Uno and three LEDs. Each LED requires a series resistor,
typically 220–330 ohms.

| Component | Arduino pin |
|---|---|
| HIGH-priority LED anode through resistor | D8 |
| MEDIUM-priority LED anode through resistor | D9 |
| LOW-priority LED anode through resistor | D10 |
| LED cathodes | GND |
| Optional compatible buzzer | D11 |

The optional buzzer is disabled by default.

## Setup

1. Install Python, VS Code and Arduino IDE.
2. Upload `arduino/AIoT_Public_Alert_Gateway.ino` to the Arduino Uno.
3. Close Arduino Serial Monitor.
4. Open the `python_test` folder in the VS Code terminal.
5. Install dependencies:

   `python -m pip install -r requirements.txt`

6. In `control.py`, set `ARDUINO_PORT` to the port shown in Arduino IDE.
7. Run the automated tests:

   `python -m unittest -v`

8. Start the voice controller:

   `python control.py`

9. Open a second terminal in `python_test` and run:

   `python -m streamlit run dashboard.py`

10. Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## How it works

1. The microphone captures a spoken announcement.
2. Google's online speech-recognition service transcribes it in Indian English.
3. `classifier.py` checks the transcript against the HIGH and MEDIUM phrase lists.
4. Python sends `H`, `M`, or `L` to the Arduino over serial.
5. The Arduino turns on the corresponding LED.
6. Python records the transcript, timestamp and priority in the CSV log.
7. Streamlit displays the saved alert history.

## Expand the vocabulary

Edit `HIGH_PHRASES` and `MEDIUM_PHRASES` in `classifier.py`.

- HIGH: immediate danger, fire, gas leak, medical emergency, violence,
  natural disaster, serious accident and other urgent hazards.
- MEDIUM: warnings, maintenance, road closures, service interruptions
  and other non-immediate issues.
- LOW: announcements that do not match either phrase list.

## Limitations

The classifier is rule-based, not a trained AI model. Speech recognition
requires internet access and can mishear speech. Keyword matching can miss
unlisted phrases or produce false positives. Negation handling is limited.

This is an educational prototype, not a certified public-safety system.
Do not rely on it as the sole means of communicating real emergencies.
