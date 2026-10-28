
import re
from typing import Iterable, Tuple


# ============================================================
# REAL-TIME VOICE-BASED ALERT CLASSIFICATION
# Rule-based classification. No trained ML model is used.
# ============================================================

HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

PRIORITY_CODES = {
    HIGH: "H",
    MEDIUM: "M",
    LOW: "L",
}


# ============================================================
# HIGH-PRIORITY PHRASES
# ============================================================

HIGH_PHRASES = [
    # General emergencies
    "emergency",
    "major emergency",
    "life threatening situation",
    "immediate danger",
    "urgent evacuation",
    "evacuate immediately",
    "evacuate the building",
    "evacuate the area",
    "leave the building immediately",
    "call emergency services",
    "emergency services are required",
    "disaster in progress",

    # Fire, smoke, gas and chemicals
    "fire",
    "fire has broken out",
    "fire has started",
    "building is on fire",
    "electrical fire",
    "flames are visible",
    "flames are spreading",
    "smoke is spreading",
    "heavy smoke",
    "thick smoke",
    "smoke filling the room",
    "smoke filling the building",
    "fire spreading",
    "uncontrolled fire",
    "explosion",
    "explosion has occurred",
    "gas leak",
    "gas is leaking",
    "gas leakage",
    "fuel leak",
    "fuel is leaking",
    "petrol leak",
    "diesel leak",
    "chemical leak",
    "chemical spill",
    "chemical container has ruptured",
    "toxic fumes",
    "fumes are spreading",
    "hazardous fumes",
    "chemical release",

    # Medical emergencies
    "medical emergency",
    "heart attack",
    "cardiac arrest",
    "not breathing",
    "struggling to breathe",
    "difficulty breathing",
    "severe chest pain",
    "unconscious",
    "unresponsive",
    "person has collapsed",
    "collapsed and unconscious",
    "severe bleeding",
    "heavy bleeding",
    "serious injury",
    "critical injury",
    "multiple people injured",
    "people have been hurt",
    "person needs urgent medical attention",
    "ambulance required",
    "ambulance is needed",
    "ambulance is urgently required",
    "seizure",
    "overdose",
    "several people are injured",
    "several people injured",

    # Violence and security
    "shots fired",
    "gunshots",
    "active shooter",
    "armed attacker",
    "violent confrontation",
    "violent attack",
    "physical assault",
    "person is attacking people",
    "weapon has been reported",
    "bomb threat",
    "bomb discovered",
    "explosive device",
    "violent disturbance",
    "people are fighting violently",
    "immediate security threat",

    # Structural and environmental emergencies
    "building collapse",
    "structure has collapsed",
    "roof has collapsed",
    "wall has collapsed",
    "ceiling collapsed",
    "ceiling has collapsed",
    "trapped beneath debris",
    "trapped beneath fallen material",
    "employee is trapped",
    "person is trapped",
    "people are trapped",
    "people trapped inside",
    "structural collapse",
    "earthquake damage",
    "strong earthquake",
    "building is shaking",
    "building is shaking after a strong earthquake",
    "severe flooding",
    "flood water entering homes",
    "water is entering nearby homes",
    "river has overflowed",
    "flash flood",
    "flooding is spreading",
    "landslide",
    "road has collapsed",
    "bridge collapse",
    "bridge structure has partially collapsed",
    "dangerous electrical contact",
    "electric shock",
    "electrocuted",
    "live electrical wire",
    "fallen power line",
    "power line has fallen",

    # Transport emergencies
    "serious road collision",
    "major road accident",
    "multiple vehicle collision",
    "multiple people injured in a collision",
    "train derailment",
    "bus has overturned",
    "vehicle has overturned",
    "vehicle has crashed into a building",
    "passenger is unconscious",
    "passenger is not responding",
    "person struck by a vehicle",
    "fuel leaking from a damaged tanker",
    "fuel is leaking from the damaged tanker",
    "damaged tanker is leaking fuel",
]


# ============================================================
# MEDIUM-PRIORITY PHRASES
# ============================================================

MEDIUM_PHRASES = [
    # General warnings
    "strong winds are expected later this evening",
    "warning",
    "caution",
    "weather advisory",
    "severe weather warning",
    "possible localised flooding",
    "possible localized flooding",
    "heavy rainfall expected",
    "strong winds expected",
    "monitor the situation",
    "precautionary measures",

    # Transport and travel
    "bus delay",
    "bus delays",
    "bus is delayed",
    "the bus is delayed",
    "bus services are delayed",
    "train delay",
    "train delays",
    "train services are delayed",
    "train services are running behind schedule",
    "services are running behind schedule",
    "traffic congestion",
    "heavy traffic",
    "traffic disruption",
    "minor traffic collision",
    "minor road accident",
    "road closure",
    "road will be closed",
    "road closed",
    "road resurfacing",
    "resurfacing work",
    "traffic diversion",
    "transport services are disrupted",
    "shuttle service has been rescheduled",
    "shuttle service is delayed",
    "service has been rescheduled",
    "public transport disruption",
    "parking spaces are unavailable",
    "parking area is closed",
    "entrance will remain closed",
    "entrance is temporarily closed",

    # Maintenance and repairs
    "maintenance",
    "scheduled maintenance",
    "routine maintenance",
    "scheduled repairs",
    "routine inspection",
    "backup generator",
    "generator inspection",
    "generator maintenance",
    "fire alarm inspection",
    "fire alarm system repair",
    "fire alarm system maintenance",
    "fire alarm testing",
    "fire alarm system repair",
    "fire detection system maintenance",
    "smoke detector maintenance",
    "equipment repair",
    "equipment maintenance",
    "repair work",
    "repair work is underway",
    "technicians are repairing",
    "system inspection",
    "inspection begins",
    "maintenance work",
    "scheduled upgrade",
    "equipment replacement",
    "minor damage",
    "minor damage has been reported",
    "roadside sign",
    "building maintenance",
    "maintenance team",
    "public announcement system",
    "announcement system is being repaired",

    # Utilities and infrastructure
    "water supply interruption",
    "water supply will be interrupted",
    "water supply will be unavailable",
    "power interruption",
    "power outage",
    "electricity interruption",
    "network outage",
    "network services may be unavailable",
    "internet service interruption",
    "service interruption",
    "temporary service interruption",
    "temporary outage",
    "scheduled outage",
    "water service disruption",
    "electricity service disruption",
    "utility services are interrupted",

    # Education and facility operations
    "classes will start late",
    "classes will be delayed",
    "classes are postponed",
    "class has been rescheduled",
    "school will open late",
    "office will open late",
    "office closure",
    "facility closure",
    "building access is restricted",
    "access is restricted",
    "area is temporarily closed",
    "area will remain closed",
    "meeting has been moved",
    "meeting has been rescheduled",
    "schedule has changed",
    "schedule change",
    "service has been delayed",
    "service is unavailable",
    "temporarily unavailable",
    "classes in block c will start thirty minutes late",
]


# ============================================================
# NEGATION HANDLING
# ============================================================

NEGATED_HAZARDS = [
    "fire",
    "smoke",
    "gas leak",
    "gas leakage",
    "fuel leak",
    "chemical leak",
    "chemical spill",
    "explosion",
    "flood",
    "flooding",
    "structural collapse",
    "heart attack",
    "cardiac arrest",
    "bomb threat",
    "active shooter",
    "shots fired",
    "serious injury",
    "medical emergency",
    "emergency",
    "immediate danger",
    "security threat",
]

NEGATION_PREFIXES = [
    r"\bno\s+(?:signs?\s+of\s+)?",
    r"\bnot\s+(?:currently\s+)?",
    r"\bwithout\s+",
    r"\bthere\s+is\s+no\s+",
    r"\bthere\s+are\s+no\s+",
    r"\bthere\s+was\s+no\s+",
    r"\bthere\s+were\s+no\s+",
    r"\bno\s+evidence\s+of\s+",
    r"\bhas\s+not\s+been\s+reported\s+",
    r"\bhas\s+not\s+occurred\s+",
    r"\bhas\s+been\s+ruled\s+out\s*:\s*",
]


# ============================================================
# CONTEXT PATTERNS
# ============================================================

ADMINISTRATIVE_PATTERNS = [
    r"\bemergency management committee\b",
    r"\bemergency planning committee\b",
    r"\bemergency response meeting\b",
    r"\bemergency preparedness meeting\b",
    r"\bemergency services meeting\b",
    r"\bemergency plan review\b",
    r"\bemergency planning session\b",
    r"\bfire safety presentation\b",
    r"\bfire safety team.{0,50}\bpresentation\b",
    r"\bpresentation.{0,50}\bfire safety\b",
    r"\bfire safety training\b",
    r"\bfire safety workshop\b",
    r"\bannual emergency plan\b",
    r"\bcommittee will review\b",
    r"\bmonthly report\b",
    r"\bpreparing a presentation\b",
    r"\bpreparing for a presentation\b",
    r"\bwill publish its report\b",
]

MAINTENANCE_CONTEXT_PATTERNS = [
    r"\bfire alarm inspection\b",
    r"\bfire alarm system repair\b",
    r"\broutine inspection of the fire alarm\b",
    r"\bfire alarm system maintenance\b",
    r"\bmaintenance of the fire alarm system\b",
    r"\bfire alarm testing\b",
    r"\btesting of the fire alarm system\b",
    r"\bfire detection system maintenance\b",
    r"\bsmoke detector maintenance\b",
    r"\broutine fire alarm inspection\b",
    r"\bscheduled fire alarm inspection\b",
]

DRILL_OR_TEST_PATTERNS = [
    r"\bfire drill\b",
    r"\bemergency drill\b",
    r"\bevacu(?:ation|ate) drill\b",
    r"\bpractice evacuation\b",
    r"\bpractising the evacuation procedure\b",
    r"\bpracticing the evacuation procedure\b",
    r"\bscheduled communication test\b",
    r"\bcommunication test\b",
    r"\bsystem test\b",
    r"\btesting announcement\b",
    r"\bthis is only a test\b",
    r"\bthis is a drill\b",
    r"\bno action is required\b",
    r"\btraining exercise\b",
    r"\bsimulation exercise\b",
    r"\bpractice exercise\b",
]

DIRECT_EMERGENCY_PATTERNS = [
    r"\bflames?\b",
    r"\bfire has (?:broken out|started)\b",
    r"\b(?:building|room|vehicle) is on fire\b",
    r"\bsmoke is (?:spreading|filling|coming out)\b",
    r"\bsmoke (?:is visible|has been detected)\b",
    r"\bexplosion\b",
    r"\b(?:gas|fuel|petrol|diesel) (?:is )?leaking\b",
    r"\b(?:gas|fuel|chemical) leak\b",
    r"\bchemical container has ruptured\b",
    r"\bfumes are spreading\b",
    r"\b(?:heart attack|cardiac arrest)\b",
    r"\bnot breathing\b",
    r"\bstruggling to breathe\b",
    r"\bsevere chest pain\b",
    r"\bunconscious\b",
    r"\bunresponsive\b",
    r"\bsevere bleeding\b",
    r"\bactive shooter\b",
    r"\bshots fired\b",
    r"\bviolent confrontation\b",
    r"\bviolent attack\b",
    r"\btrapped beneath\b",
    r"\bperson is trapped\b",
    r"\bpeople are trapped\b",
    r"\bbuilding collapse\b",
    r"\bstructure has collapsed\b",
    r"\bceiling collapsed\b",
    r"\bceiling has collapsed\b",
    r"\bseveral people are injured\b",
    r"\bseveral people injured\b",
    r"\bambulance is urgently required\b",
    r"\bambulance required\b",
    r"\bbridge structure has partially collapsed\b",
    r"\bbridge.{0,30}\bpartially collapsed\b",
    r"\bbuilding is shaking after a strong earthquake\b",
    r"\bbuilding is shaking\b",
    r"\briver has overflowed\b",
    r"\bflood water (?:is )?entering\b",
    r"\bwater is entering nearby homes\b",
    r"\bflash flood\b",
    r"\bmultiple people (?:have been )?injured\b",
    r"\bserious road collision\b",
    r"\bmajor road accident\b",
    r"\bfuel leaking from\b",
    r"\bperson struck by a vehicle\b",
    r"\belectrocuted\b",
    r"\belectric shock\b",
    r"\blive electrical wire\b",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text: str) -> str:
    """Normalize text for case-insensitive matching."""
    if text is None:
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_phrase(text: str, phrase: str) -> bool:
    """Match a phrase without matching it inside a larger word."""
    normalized_text = normalize_text(text)
    normalized_phrase = normalize_text(phrase)

    if not normalized_text or not normalized_phrase:
        return False

    pattern = (
        r"(?<!\w)"
        + re.escape(normalized_phrase)
        + r"(?!\w)"
    )
    return re.search(pattern, normalized_text) is not None


def matches_any(text: str, phrases: Iterable[str]) -> bool:
    """Return True if any phrase matches."""
    return any(contains_phrase(text, phrase) for phrase in phrases)


def matches_patterns(text: str, patterns: Iterable[str]) -> bool:
    """Return True if any regular expression matches."""
    normalized_text = normalize_text(text)
    return any(
        re.search(pattern, normalized_text) is not None
        for pattern in patterns
    )


def remove_negated_hazards(text: str) -> str:
    """
    Remove explicitly negated hazard phrases while preserving
    unrelated text that may describe another active emergency.
    """
    result = normalize_text(text)

    for hazard in sorted(NEGATED_HAZARDS, key=len, reverse=True):
        escaped_hazard = re.escape(hazard)

        for prefix in NEGATION_PREFIXES:
            pattern = prefix + escaped_hazard + r"\b"
            result = re.sub(pattern, " ", result)

    return re.sub(r"\s+", " ", result).strip()


# ============================================================
# MAIN CLASSIFIER
# ============================================================

def classify_announcement(text: str) -> Tuple[str, str]:
    """
    Return (priority, Arduino serial code).

    HIGH   -> ("HIGH", "H")
    MEDIUM -> ("MEDIUM", "M")
    LOW    -> ("LOW", "L")
    """
    original_text = normalize_text(text)

    if not original_text:
        return LOW, PRIORITY_CODES[LOW]

    cleaned_text = remove_negated_hazards(original_text)

    if not cleaned_text:
        return LOW, PRIORITY_CODES[LOW]

    # Active emergencies must take precedence over routine contexts.
    if matches_patterns(cleaned_text, DIRECT_EMERGENCY_PATTERNS):
        return HIGH, PRIORITY_CODES[HIGH]

    # Routine fire-alarm inspection or repair is MEDIUM, not HIGH.
    if matches_patterns(cleaned_text, MAINTENANCE_CONTEXT_PATTERNS):
        return MEDIUM, PRIORITY_CODES[MEDIUM]

    # Routine administrative references are not active emergencies.
    if matches_patterns(cleaned_text, ADMINISTRATIVE_PATTERNS):
        return LOW, PRIORITY_CODES[LOW]

    # Drills and tests are LOW unless a direct emergency was detected.
    if matches_patterns(cleaned_text, DRILL_OR_TEST_PATTERNS):
        return LOW, PRIORITY_CODES[LOW]

    # General phrase-library matching.
    if matches_any(cleaned_text, HIGH_PHRASES):
        return HIGH, PRIORITY_CODES[HIGH]

    if matches_any(cleaned_text, MEDIUM_PHRASES):
        return MEDIUM, PRIORITY_CODES[MEDIUM]

    return LOW, PRIORITY_CODES[LOW]


# ============================================================
# MANUAL TEST
# Run: python classifier.py
# ============================================================

if __name__ == "__main__":
    sample_announcements = [
        "Flames are visible near the electrical control panel",
        "The river has overflowed and water is entering nearby homes",
        "A chemical container has ruptured and fumes are spreading",
        "An employee is trapped beneath fallen construction material",
        "A person is having severe chest pain and struggling to breathe",
        "A violent confrontation is taking place near the gate",
        "Multiple people have been hurt in a serious road collision",
        "Fuel is leaking from the damaged tanker",
        "Several people are injured after the ceiling collapsed",
        "An ambulance is urgently required at the main entrance",
        "The bridge structure has partially collapsed",
        "The building is shaking after a strong earthquake",
        "Bus services are delayed because of heavy traffic",
        "The bus is delayed",
        "Routine inspection of the backup generator begins this afternoon",
        "The east entrance will remain closed for scheduled repairs",
        "Water supply will be interrupted for two hours tomorrow",
        "Train services are running behind schedule",
        "Notice: fire alarm inspection",
        "Notice: fire alarm system repair",
        "The fire safety team is preparing a presentation for students",
        "Students are practising the evacuation procedure as part of a drill",
        "The emergency management committee will review its annual plan",
        "There is no fire in the building",
        "There is no fire, but a person is not breathing",
        "",
    ]

    for announcement in sample_announcements:
        priority, code = classify_announcement(announcement)
        display_text = announcement or "[empty announcement]"
        print(f"{priority:6} | {code} | {display_text}")
