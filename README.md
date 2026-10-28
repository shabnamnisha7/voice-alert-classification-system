# Real-Time Voice-Based Alert Classification Using Python and Arduino

A real-time voice-based alert classification system that processes spoken announcements, assigns priority levels using rule-based text classification, controls Arduino LED indicators, and records alerts for monitoring through a Streamlit dashboard.

## Overview

The system combines Python, speech recognition, Arduino Uno, and a web-based dashboard to demonstrate how spoken announcements can be converted into actionable priority alerts.

When a user speaks an announcement, the Python application converts the speech into text, classifies its priority, records the result in a CSV file, and sends a corresponding command to the Arduino over serial communication.

The Arduino then activates the LED associated with the assigned priority.

## Key Features

- **Voice input:** Captures spoken announcements through a microphone.
- **Speech-to-text:** Uses the SpeechRecognition library with Google's online speech recognition service.
- **Priority classification:** Assigns HIGH, MEDIUM, or LOW priority using rule-based phrase matching.
- **Arduino integration:** Communicates with an Arduino Uno through serial commands.
- **Hardware indicators:** Uses separate LEDs to represent the three priority levels.
- **Alert logging:** Stores timestamps, recognized announcements, and priority levels in a CSV file.
- **Interactive dashboard:** Displays alert statistics, priority distribution, and recent announcements.
- **Search and filtering:** Supports searching recorded announcements and filtering by priority.
- **CSV export:** Allows dashboard records to be downloaded for further analysis.
- **Automated testing:** Includes unit tests and evaluation scripts for checking classifier behavior.

## System Architecture

```text
Spoken Announcement
        |
        v
Microphone Input
        |
        v
Python Speech Recognition
        |
        v
Recognized Text
        |
        v
Rule-Based Classification
        |
        +----------------------+
        |                      |
        v                      v
CSV Alert Logging       Serial Communication
                               |
                               v
                          Arduino Uno
                               |
                    +----------+----------+
                    |          |          |
                    v          v          v
                 HIGH LED   MEDIUM LED   LOW LED

Python Alert History
        |
        v
Streamlit Dashboard
        |
        v
Statistics, Search, Filtering
and CSV Export
```

## Technologies Used

| Component | Technology |
|---|---|
| Programming language | Python |
| Hardware controller | Arduino Uno |
| Embedded programming | Arduino C/C++ |
| Speech recognition | SpeechRecognition |
| Serial communication | PySerial |
| Dashboard | Streamlit |
| Data handling | Pandas |
| Data storage | CSV |
| Testing | Python unittest |

## Project Structure

```text
Real-Time Voice-Based Alert Classification/
|
|-- README.md
|-- .gitignore
|
|-- arduino/
|   |-- AIoT_Public_Alert_Gateway/
|       |-- AIoT_Public_Alert_Gateway.ino
|
|-- python_test/
    |-- README.md
    |-- classifier.py
    |-- control.py
    |-- dashboard.py
    |-- test_classifier.py
    |-- evaluate_classifier.py
    |-- evaluate_unseen_test.py
    |-- evaluation_dataset.csv
    |-- unseen_test_set.csv
    |-- unseen_test_results.csv
    |-- requirements.txt
```

## Hardware Requirements

- Arduino Uno
- USB cable for Arduino communication
- Computer with a microphone
- Three LEDs for HIGH, MEDIUM, and LOW priorities
- Appropriate current-limiting resistors
- Breadboard and jumper wires

An optional buzzer module is supported by the Arduino sketch but is disabled by default.

### LED Connections

| Component | Arduino pin |
|---|---|
| HIGH priority LED | D8 |
| MEDIUM priority LED | D9 |
| LOW priority LED | D10 |
| Optional buzzer | D11 |

Connect each LED with an appropriate current-limiting resistor. Connect the LED cathodes to GND.

## Software Requirements

- Python 3.11 or a compatible Python version
- Arduino IDE
- Git
- A microphone
- Internet access for Google's online speech recognition service
- A supported serial port for the Arduino

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shabnamnisha7/voice-alert-classification-system.git
cd voice-alert-classification-system
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r python_test/requirements.txt
```

If microphone access fails because PyAudio is unavailable, resolve the PyAudio installation issue for your Python and operating system before running the application.

### 4. Upload the Arduino Sketch

1. Open `arduino/AIoT_Public_Alert_Gateway/AIoT_Public_Alert_Gateway.ino` in Arduino IDE.
2. Connect the Arduino Uno using USB.
3. Select the correct board and serial port.
4. Upload the sketch.
5. Close the Arduino Serial Monitor before running the Python application, because the serial port generally cannot be shared by both programs.

### 5. Configure the Serial Port

Open `python_test/control.py` and check these settings:

```python
ARDUINO_PORT = "COM3"
BAUD_RATE = 9600
LANGUAGE = "en-IN"
```

Replace `COM3` with the port assigned to your Arduino if necessary.

### 6. Run the Voice Classification Application

From the repository root:

```powershell
python python_test/control.py
```

Allow microphone access when prompted. Speak a short announcement and check the printed classification, CSV log, and corresponding LED.

The application supports the configured exit phrases `quit program`, `exit program`, and `stop listening`.

### 7. Launch the Dashboard

Open a second terminal, activate the same virtual environment, and run:

```powershell
python -m streamlit run python_test/dashboard.py
```

Open the local URL displayed in the terminal by Streamlit.

The dashboard reads the alert history from `python_test/alert_history.csv`. The file is generated by the voice application and is intentionally excluded from Git tracking to avoid publishing local announcement logs.

## Dashboard Features

The dashboard uses a responsive Bento Grid-style layout and includes:

- Project title and system overview
- Total alert count and priority metrics
- Priority distribution visualizations
- HIGH priority percentage and other summary statistics
- Recent alert records
- Priority-based filtering
- Announcement search
- Newest-first sorting
- CSV download
- Light and dark appearance support where available

For meaningful live monitoring, run the voice application first so that the alert history file exists and contains records.

## Classification Logic

The classifier in `python_test/classifier.py` uses predefined phrases and keywords to assign one of three priority levels.

| Priority | Meaning | System response |
|---|---|---|
| HIGH | Urgent or emergency-related announcement recognized by configured rules | HIGH LED activated |
| MEDIUM | Announcement matching the configured medium-priority rules | MEDIUM LED activated |
| LOW | Announcement matching the configured low-priority rules or the classifier's fallback behavior | LOW LED activated |

The exact classification depends on the rules defined in the source code.

**Important:** This project uses rule-based classification, not a trained machine learning model. It is a prototype for demonstrating speech processing, rule-based decision-making, serial communication, and hardware indication. It is not a certified emergency warning system.

## Arduino Serial Protocol

The Python application sends priority commands to the Arduino over a serial connection at 9600 baud.

| Command | Action |
|---|---|
| `H` | Activate HIGH priority indication |
| `M` | Activate MEDIUM priority indication |
| `L` | Activate LOW priority indication |
| `Q` | Turn off the alert indicators |

The Arduino sketch also sends acknowledgement messages for the supported commands.

## Testing and Evaluation

The repository includes separate testing and evaluation tools.

### Unit Tests

Run the classifier tests from the repository root:

```powershell
python -m unittest discover -s python_test -p "test_classifier.py" -v
```

The project has previously passed 14 unit tests. Run the tests again after changing the classifier to confirm its current behavior.

### Evaluation Dataset

Run the primary classifier evaluation:

```powershell
python python_test/evaluate_classifier.py
```

The included evaluation dataset contains 60 labeled examples, with 20 examples per priority class. A previous evaluation reported 60 correct classifications out of 60 on this dataset.

This result measures performance on the included dataset only. It does not establish real-world accuracy.

### Unseen Test Set

Run the separate evaluation script:

```powershell
python python_test/evaluate_unseen_test.py
```

The project includes an exploratory test set and previously generated results. These files can be used to inspect classification behavior beyond the primary dataset, but they are not an independently validated benchmark.

## Limitations

- Classification depends on manually defined phrases and keywords.
- Unfamiliar wording, accents, background noise, and speech recognition errors may produce incorrect classifications.
- Online speech recognition requires internet access.
- The serial port must be configured correctly.
- The dashboard depends on the CSV alert history generated by the Python application.
- Evaluation results on small, predefined datasets may not reflect real-world performance.
- The system has not been validated for use as a life-safety or emergency communication device.

## Future Improvements

- Improve classification rules using broader, independently labeled datasets.
- Add confidence scores and explicit handling of uncertain speech recognition.
- Introduce a trained text classification model and compare it with the rule-based baseline.
- Add serial connection status and hardware acknowledgement monitoring to the dashboard.
- Improve error handling for microphone, network, and Arduino connection failures.
- Evaluate the classifier on independently collected speech samples under different noise conditions.
- Add persistent configuration for serial ports and classification thresholds.

## Learning Outcomes

This project demonstrates practical integration of:

- Python application development
- Speech recognition
- Text processing and rule-based classification
- Serial communication between a computer and a microcontroller
- Arduino GPIO control
- CSV-based data logging
- Streamlit dashboard development
- Unit testing and dataset-based evaluation
- Git and GitHub version control

## Author

**Shabnam Nisha**

B.Tech Electronics and Communication Engineering

GitHub: [@shabnamnisha7](https://github.com/shabnamnisha7)

## License

No license has been specified yet. Unless a license is added to the repository, reuse and redistribution remain subject to applicable copyright law.
