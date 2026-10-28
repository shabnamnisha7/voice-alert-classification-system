import csv
from collections import Counter

from classifier import classify_announcement

DATASET_PATH = "unseen_test_set.csv"
RESULTS_PATH = "unseen_test_results.csv"
LABELS = ["HIGH", "MEDIUM", "LOW"]


def get_priority(result):
    """Support classifiers that return either 'HIGH' or ('HIGH', 'H')."""
    if isinstance(result, (tuple, list)):
        return str(result[0]).upper()
    return str(result).upper()


def main():
    with open(DATASET_PATH, "r", newline="", encoding="utf-8-sig") as file:
        dataset = list(csv.DictReader(file))

    if not dataset:
        raise ValueError(f"No test rows found in {DATASET_PATH}")

    required_columns = {"text", "expected_priority"}
    if not required_columns.issubset(dataset[0].keys()):
        raise ValueError(
            f"{DATASET_PATH} must contain columns: text, expected_priority"
        )

    results = []
    correct = 0
    confusion = {expected: {predicted: 0 for predicted in LABELS} for expected in LABELS}

    for row in dataset:
        text = row["text"].strip()
        expected = row["expected_priority"].strip().upper()
        predicted = get_priority(classify_announcement(text))
        is_correct = predicted == expected
        correct += int(is_correct)

        if expected in LABELS and predicted in LABELS:
            confusion[expected][predicted] += 1

        results.append({
            "text": text,
            "expected_priority": expected,
            "predicted_priority": predicted,
            "correct": is_correct,
        })

    total = len(results)
    print("=" * 68)
    print("UNSEEN VOICE ALERT CLASSIFIER TEST")
    print("=" * 68)
    print(f"Total announcements : {total}")
    print(f"Correct predictions : {correct}")
    print(f"Accuracy            : {correct / total * 100:.2f}%")

    print("\nPER-CLASS METRICS")
    print(f"{'Priority':<10}{'Precision':>12}{'Recall':>12}{'F1-score':>12}{'Samples':>10}")
    print("-" * 56)

    for label in LABELS:
        tp = confusion[label][label]
        predicted_count = sum(confusion[expected][label] for expected in LABELS)
        actual_count = sum(confusion[label].values())
        precision = tp / predicted_count if predicted_count else 0.0
        recall = tp / actual_count if actual_count else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        print(
            f"{label:<10}{precision * 100:>11.2f}%{recall * 100:>11.2f}%"
            f"{f1 * 100:>11.2f}%{actual_count:>10}"
        )

    print("\nCONFUSION MATRIX (rows = expected, columns = predicted)")
    print(f"{'Expected':<12}{'HIGH':>10}{'MEDIUM':>10}{'LOW':>10}")
    for expected in LABELS:
        print(
            f"{expected:<12}"
            + "".join(f"{confusion[expected][predicted]:>10}" for predicted in LABELS)
        )

    incorrect = [row for row in results if not row["correct"]]
    print("\nINCORRECT PREDICTIONS")
    if incorrect:
        for row in incorrect:
            print(f"- Expected {row['expected_priority']}, got {row['predicted_priority']}: {row['text']}")
    else:
        print("No incorrect predictions.")

    high_misses = sum(
        1 for row in results
        if row["expected_priority"] == "HIGH" and row["predicted_priority"] != "HIGH"
    )
    print(f"\nHIGH-priority misses: {high_misses}")

    with open(RESULTS_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["text", "expected_priority", "predicted_priority", "correct"],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Detailed results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()

