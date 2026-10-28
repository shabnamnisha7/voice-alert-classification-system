
import unittest

from classifier import (
    HIGH_PHRASES,
    MEDIUM_PHRASES,
    classify_announcement,
)


class ClassifierTests(unittest.TestCase):

    def check(self, text, expected):
        result = classify_announcement(text)
        self.assertEqual(
            result,
            expected,
            msg=f"Unexpected classification for: {text!r}",
        )

    # ---------------------------------------------------------
    # Basic input tests
    # ---------------------------------------------------------

    def test_empty_input(self):
        self.check("", ("LOW", "L"))
        self.check("   ", ("LOW", "L"))

    def test_low(self):
        self.check("The event starts at ten", ("LOW", "L"))
        self.check("The library has new books", ("LOW", "L"))
        self.check("No fire has been reported", ("LOW", "L"))

    # ---------------------------------------------------------
    # HIGH-priority announcements
    # ---------------------------------------------------------

    def test_high_general_and_fire(self):
        self.check(
            "There is a fire near the main entrance",
            ("HIGH", "H"),
        )
        self.check("This is an emergency", ("HIGH", "H"))
        self.check(
            "Someone is having a heart attack, call an ambulance",
            ("HIGH", "H"),
        )
        self.check("A person is trapped inside", ("HIGH", "H"))
        self.check("Shots fired near the gate", ("HIGH", "H"))

    def test_high_wins_if_another_emergency_is_present(self):
        self.check(
            "A power outage occurred and there is a gas leak",
            ("HIGH", "H"),
        )

    def test_all_high_phrases_are_recognized(self):
        for phrase in HIGH_PHRASES:
            with self.subTest(phrase=phrase):
                self.check(
                    f"Alert: {phrase}",
                    ("HIGH", "H"),
                )

    # ---------------------------------------------------------
    # MEDIUM-priority announcements
    # ---------------------------------------------------------

    def test_medium(self):
        self.check("The bus is delayed", ("MEDIUM", "M"))
        self.check("BUS DELAY.", ("MEDIUM", "M"))
        self.check(
            "Maintenance is in progress",
            ("MEDIUM", "M"),
        )
        self.check("There is a power outage", ("MEDIUM", "M"))

    def test_all_medium_phrases_are_recognized(self):
        for phrase in MEDIUM_PHRASES:
            with self.subTest(phrase=phrase):
                self.check(
                    f"Notice: {phrase}",
                    ("MEDIUM", "M"),
                )

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def test_case_and_punctuation(self):
        self.check("FIRE NEAR THE GATE!", ("HIGH", "H"))
        self.check("BUS DELAY.", ("MEDIUM", "M"))
        self.check("   ", ("LOW", "L"))

    # ---------------------------------------------------------
    # Negation
    # ---------------------------------------------------------

    def test_simple_negation(self):
        self.check("No fire has been reported", ("LOW", "L"))
        self.check("There is no gas leak", ("LOW", "L"))
        self.check("There is no smoke", ("LOW", "L"))

    def test_negation_does_not_hide_another_emergency(self):
        self.check(
            "No fire has been reported, but there is a gas leak",
            ("HIGH", "H"),
        )
        self.check(
            "There is no fire, but smoke is spreading through the building",
            ("HIGH", "H"),
        )

    # ---------------------------------------------------------
    # Drills and tests
    # ---------------------------------------------------------

    def test_drill_and_test_announcements(self):
        self.check("This is a fire drill", ("LOW", "L"))
        self.check("This is only a test", ("LOW", "L"))
        self.check("A false alarm was reported", ("LOW", "L"))

    def test_drill_with_separate_emergency(self):
        self.check(
            "Fire drill today, but a gas leak has been reported",
            ("HIGH", "H"),
        )
        self.check(
            "This is a fire drill, but a real gas leak has been reported",
            ("HIGH", "H"),
        )

    # ---------------------------------------------------------
    # Context-sensitive cases
    # ---------------------------------------------------------

    def test_maintenance_about_fire_alarm(self):
        self.check(
            "Fire alarm system maintenance is in progress",
            ("MEDIUM", "M"),
        )

    def test_administrative_emergency_reference(self):
        self.check(
            "The emergency management committee will meet tomorrow",
            ("LOW", "L"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
