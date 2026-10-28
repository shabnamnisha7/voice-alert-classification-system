
import csv
from pathlib import Path

from classifier import classify_announcement


BASE_DIR = Path(__file__).resolve().parent
DATASET_FILE = BASE_DIR / "evaluation_dataset.csv"
RESULTS_FILE = BASE_DIR / "evaluation_results.csv"

CLASSES = ["HIGH", "MEDIUM", "LOW"]


def normalize_prediction(result, announcement):
    """Support classifiers returning either a label or (label, code)."""

    if isinstance(result, (tuple, list)):
        if not result:
            raise ValueError(
                f"Classifier returned an empty result for: {announcement}"
            )
        result = result[0]

    if not isinstance(result, str):
        raise ValueError(
            f"Unexpected classifier result {result!r} "
            f"for: {announcement}"
        )

    priority = result.strip().upper()

    if priority not in CLASSES:
        raise ValueError(
            f"Classifier returned invalid priority {result!r} "
            f"for: {announcement}"
        )

    return priority


def load_dataset(path):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    records = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"text", "expected_priority"}

        if not reader.fieldnames or not required.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                "CSV must contain columns: text, expected_priority"
            )

        for row_number, row in enumerate(reader, start=2):
            announcement = (row.get("text") or "").strip()
            expected = (
                row.get("expected_priority") or ""
            ).strip().upper()

            if not announcement:
                raise ValueError(
                    f"Empty announcement on CSV row {row_number}"
                )

            if expected not in CLASSES:
                raise ValueError(
                    f"Invalid expected priority {expected!r} "
                    f"on CSV row {row_number}"
                )

            records.append({
                "text": announcement,
                "expected_priority": expected,
            })

    if not records:
        raise ValueError("The evaluation dataset is empty.")

    return records


def evaluate(records):
    confusion = {
        actual: {predicted: 0 for predicted in CLASSES}
        for actual in CLASSES
    }
    results = []

    for record in records:
        expected = record["expected_priority"]
        announcement = record["text"]

        raw_result = classify_announcement(announcement)
        predicted = normalize_prediction(raw_result, announcement)

        correct = predicted == expected
        confusion[expected][predicted] += 1

        results.append({
            "text": announcement,
            "expected_priority": expected,
            "predicted_priority": predicted,
            "correct": correct,
        })

    total = len(results)
    correct_count = sum(row["correct"] for row in results)
    accuracy = correct_count / total

    metrics = {}

    for label in CLASSES:
        true_positive = confusion[label][label]
        actual_count = sum(confusion[label].values())
        predicted_count = sum(
            confusion[actual][label] for actual in CLASSES
        )

        precision = (
            true_positive / predicted_count
            if predicted_count else 0.0
        )
        recall = (
            true_positive / actual_count
            if actual_count else 0.0
        )
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall else 0.0
        )

        metrics[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": actual_count,
        }

    return results, confusion, metrics, accuracy


def save_results(results):
    fields = [
        "text",
        "expected_priority",
        "predicted_priority",
        "correct",
    ]

    with RESULTS_FILE.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)


def print_report(results, confusion, metrics, accuracy):
    print("\n" + "=" * 70)
    print("VOICE ALERT CLASSIFIER EVALUATION")
    print("=" * 70)
    print(f"Total announcements : {len(results)}")
    print(f"Correct predictions : {sum(r['correct'] for r in results)}")
    print(f"Accuracy            : {accuracy:.2%}")

    print("\nPER-CLASS METRICS")
    print(
        f"{'Priority':<12}{'Precision':>12}"
        f"{'Recall':>12}{'F1-score':>12}{'Samples':>10}"
    )
    print("-" * 58)

    for label in CLASSES:
        m = metrics[label]
        print(
            f"{label:<12}{m['precision']:>11.2%}"
            f"{m['recall']:>12.2%}{m['f1']:>12.2%}"
            f"{m['support']:>10}"
        )

    print("\nCONFUSION MATRIX")
    print("Rows = expected; columns = predicted")
    print(f"{'Expected':<12}{'HIGH':>10}{'MEDIUM':>10}{'LOW':>10}")
    print("-" * 42)

    for actual in CLASSES:
        print(
            f"{actual:<12}"
            f"{confusion[actual]['HIGH']:>10}"
            f"{confusion[actual]['MEDIUM']:>10}"
            f"{confusion[actual]['LOW']:>10}"
        )

    high_misses = [
        r for r in results
        if r["expected_priority"] == "HIGH"
        and r["predicted_priority"] != "HIGH"
    ]

    print("\nCRITICAL HIGH-PRIORITY MISSES")
    print(f"Count: {len(high_misses)}")

    for index, row in enumerate(high_misses, start=1):
        print(
            f"{index}. Predicted {row['predicted_priority']}: "
            f"{row['text']}"
        )

    errors = [r for r in results if not r["correct"]]

    print("\nINCORRECT PREDICTIONS")
    if not errors:
        print("No incorrect predictions.")
    else:
        for index, row in enumerate(errors, start=1):
            print(
                f"{index}. Expected {row['expected_priority']}, "
                f"predicted {row['predicted_priority']}: {row['text']}"
            )

    print(f"\nDetailed CSV: {RESULTS_FILE}")
    print("=" * 70)


def main():
    try:
        records = load_dataset(DATASET_FILE)
        results, confusion, metrics, accuracy = evaluate(records)
        save_results(results)
        print_report(results, confusion, metrics, accuracy)
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"\nEvaluation failed: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
