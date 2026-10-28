
"""Voice controller for Real-Time Voice-Based Alert Classification."""
import csv
import time
from datetime import datetime
from pathlib import Path

import serial
import speech_recognition as sr

from classifier import classify_announcement

ARDUINO_PORT = "COM3"  # Change this if your Arduino uses another port.
BAUD_RATE = 9600
LANGUAGE = "en-IN"

LOG_FILE = Path(__file__).resolve().parent / "alert_history.csv"

LISTEN_TIMEOUT_SECONDS = 10
PHRASE_TIME_LIMIT_SECONDS = 8

recognizer = sr.Recognizer()


def save_alert(announcement: str, priority: str) -> None:
    """Save the recognized announcement and priority to CSV."""
    file_exists = LOG_FILE.exists() and LOG_FILE.stat().st_size > 0

    try:
        with LOG_FILE.open(
            "a",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Timestamp", "Announcement", "Priority"])

            writer.writerow([
                datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                announcement,
                priority,
            ])

    except PermissionError:
        print("ERROR: Close alert_history.csv in Excel and try again.")


def main() -> None:
    arduino = None

    try:
        arduino = serial.Serial(
            ARDUINO_PORT,
            BAUD_RATE,
            timeout=2,
        )

        # Opening the serial port normally resets an Arduino Uno.
        time.sleep(2)

        print("=" * 68)
        print("REAL-TIME VOICE-BASED ALERT CLASSIFICATION")
        print("English speech | Rule-based priority | Arduino LED alerts")
        print(f"Arduino connected: {ARDUINO_PORT} at {BAUD_RATE} baud")
        print("Speak clearly in English.")
        print("Say 'quit program', 'exit program', or 'stop listening' to exit.")
        print("Google speech recognition requires an internet connection.")
        print("Add more emergency phrases in classifier.py.")
        print("=" * 68)

        with sr.Microphone() as source:
            print("Calibrating microphone. Stay quiet for one second...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("System ready.")

            while True:
                try:
                    print("\nListening...")

                    audio = recognizer.listen(
                        source,
                        timeout=LISTEN_TIMEOUT_SECONDS,
                        phrase_time_limit=PHRASE_TIME_LIMIT_SECONDS,
                    )

                    announcement = recognizer.recognize_google(
                        audio,
                        language=LANGUAGE,
                    ).strip()

                    print(f"Recognized announcement: {announcement}")

                    exit_phrases = {
                        "quit program",
                        "exit program",
                        "stop listening",
                    }

                    if " ".join(announcement.lower().split()) in exit_phrases:
                        print("Exit command detected.")
                        break

                    priority, command = classify_announcement(announcement)

                    print(f"Assigned priority: {priority} (command {command})")

                    save_alert(announcement, priority)

                    arduino.write(command.encode("ascii"))
                    arduino.flush()

                    response = (
                        arduino.readline()
                        .decode("utf-8", errors="ignore")
                        .strip()
                    )

                    if response:
                        print(f"Arduino response: {response}")

                except sr.WaitTimeoutError:
                    print("No speech detected. Speak closer to the microphone.")

                except sr.UnknownValueError:
                    print("Speech was not understood. Please repeat clearly.")

                except sr.RequestError as error:
                    print(f"Speech recognition service error: {error}")
                    print("Check your internet connection.")
                    break

    except KeyboardInterrupt:
        print("\nStopped by keyboard.")

    except serial.SerialException as error:
        print(f"Arduino connection error: {error}")
        print("Check the USB cable and COM port.")
        print("Close Arduino Serial Monitor before running this program.")

    except (OSError, AttributeError) as error:
        print(f"Microphone/audio device error: {error}")
        print("Check Windows microphone permissions and your input device.")

    finally:
        if arduino is not None and arduino.is_open:
            try:
                arduino.write(b"Q")
                arduino.flush()
            except serial.SerialException:
                pass

            arduino.close()

        print("Controller stopped. LEDs should be off.")


if __name__ == "__main__":
    main()
