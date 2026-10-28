# Multilingual Real-Time Voice-Based Alert Classification Using Python and Arduino

This prototype listens for spoken public announcements in English or Hindi, transcribes the audio using Google's online speech-recognition service, classifies the transcript with English/Hindi/Roman-Hindi keyword rules, logs it to CSV, and sends H/M/L commands to an Arduino Uno.

## Folder structure

- `python_test/control.py`: microphone, dual-language transcription, CSV logging, Arduino serial commands
- `python_test/classifier.py`: emergency vocabulary and priority rules
- `python_test/test_classifier.py`: offline classifier tests
- `python_test/dashboard.py`: Streamlit alert-history dashboard
- `python_test/requirements.txt`: Python dependencies
- `arduino/AIoT_Public_Alert_Gateway.ino`: Arduino LED controller

## Setup on Windows

1. Install Python 3.10 or 3.11 and Arduino IDE.
2. Connect the Uno and upload `arduino/AIoT_Public_Alert_Gateway.ino`.
3. In VS Code, open a terminal inside `python_test`.
4. Install dependencies: `python -m pip install -r requirements.txt`.
5. Change `ARDUINO_PORT = "COM3"` in `control.py` if your Uno uses another COM port.
6. Test the classifier offline: `python -m unittest -v`.
7. Start the voice controller: `python control.py`.
8. In a second terminal in the same folder, start the dashboard: `python -m streamlit run dashboard.py`.

## Languages

The controller attempts speech transcription with both `en-IN` and `hi-IN`. The classifier recognizes many English phrases, Hindi in Devanagari, and selected Roman-Hindi phrases. Add more vocabulary to `HIGH_PHRASES` or `MEDIUM_PHRASES` in `classifier.py`.

## Hardware mapping

- HIGH LED: D8
- MEDIUM LED: D9
- LOW LED: D10
- Optional buzzer: D11 (disabled by default)
- Serial baud rate: 9600

## Important limitations

This is a keyword/rule-based student prototype, not a trained AI model or certified emergency-dispatch system. It requires an internet connection for Google's speech-recognition service. Trying two language models can increase latency and may produce incorrect transcripts. Keyword matching can miss paraphrases or create false positives. Never use this prototype as the sole method for handling real emergencies.
