"""
Cognitive Dissonance Tracker
-----------------------------
Records daily cognitive dissonance entries and generates trend charts.

Key robustness features:
- Input validation with retry (never crashes on bad input)
- Graceful Ctrl+C handling during data entry
- Duplicate-entry prevention per day (with overwrite confirmation)
- Note sanitization (escapes commas and newlines so the CSV never breaks)
- dataclass + Enum model for entries and interpretation levels
- 7-day moving average on the chart to see real trend vs daily noise
- Streak detection for sustained high-dissonance periods
- Headless-safe plotting (won't crash on servers/cron jobs without a display)
- Corrupted CSV rows are skipped and reported, not fatal
- Configurable file paths via CLI args
"""

import argparse
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from statistics import mean

import matplotlib
import matplotlib.pyplot as plt

DEFAULT_DATA_FILE = Path("dissonance_history.csv")
DEFAULT_PLOT_FILE = Path("dissonance_trend.png")
FIELDNAMES = ["Date", "Importance", "Actions", "Discomfort", "Dissonance", "Note"]
HIGH_DISSONANCE_THRESHOLD = 6.0


class DissonanceLevel(Enum):
    LOW = (0, 3, "Great alignment! Your actions matched your beliefs.")
    MODERATE = (3, 6, "Moderate dissonance. Some contradictions are causing mild discomfort.")
    HIGH = (6, 10.1, "High dissonance! Your actions are highly misaligned with your values.")

    @classmethod
    def from_score(cls, score: float) -> "DissonanceLevel":
        for level in cls:
            low, high, _ = level.value
            if low <= score < high:
                return level
        return cls.HIGH

    @property
    def message(self) -> str:
        return self.value[2]


@dataclass
class Entry:
    date: str
    importance: int
    actions: int
    discomfort: int
    dissonance: float
    note: str

    @classmethod
    def from_inputs(cls, importance: int, actions: int, discomfort: int, note: str) -> "Entry":
        action_gap = max(0, importance - actions)
        dissonance = round((action_gap + discomfort) / 2, 1)
        return cls(
            date=datetime.now().strftime("%Y-%m-%d"),
            importance=importance,
            actions=actions,
            discomfort=discomfort,
            dissonance=dissonance,
            note=note.replace(",", ";").replace("\n", " ").replace("\r", " ").strip(),
        )


class DissonanceStorage:
    def __init__(self, path: Path = DEFAULT_DATA_FILE):
        self.path = path

    def _read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def has_entry_for(self, date_str: str) -> bool:
        return any(row["Date"] == date_str for row in self._read_all())

    def save(self, entry: Entry, overwrite: bool = False) -> None:
        rows = self._read_all()
        if overwrite:
            rows = [r for r in rows if r["Date"] != entry.date]
        rows.append(asdict_capitalized(entry))
        with self.path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)

    def load_entries(self) -> list[Entry]:
        entries = []
        for row in self._read_all():
            try:
                entries.append(
                    Entry(
                        date=row["Date"],
                        importance=int(row["Importance"]),
                        actions=int(row["Actions"]),
                        discomfort=int(row["Discomfort"]),
                        dissonance=float(row["Dissonance"]),
                        note=row.get("Note", ""),
                    )
                )
            except (KeyError, ValueError):
                print(f"Corrupted row ignored: {row}")
        return entries


def asdict_capitalized(entry: Entry) -> dict:
    """Converts the dataclass to a dict with the CSV's capitalized keys."""
    d = asdict(entry)
    return {
        "Date": d["date"],
        "Importance": d["importance"],
        "Actions": d["actions"],
        "Discomfort": d["discomfort"],
        "Dissonance": d["dissonance"],
        "Note": d["note"],
    }


def ask_int(prompt: str, low: int = 1, high: int = 10) -> int:
    """Asks for an integer within a range, retrying on invalid input."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"  -> Please enter an integer between {low} and {high}.")
            continue
        if not (low <= value <= high):
            print(f"  -> Value must be between {low} and {high}.")
            continue
        return value


def record_entry(storage: DissonanceStorage) -> None:
    print("\n--- Daily Cognitive Dissonance Tracker ---")
    print("\nThink about your main goal, belief, or value today (e.g., productivity, health, patience).")

    try:
        importance = ask_int("1. How important was this value to you today? (1-10): ")
        actions = ask_int("2. How well did your actions align with this value? (1-10): ")
        discomfort = ask_int("3. What level of inner discomfort/frustration did you feel? (1-10): ")
        note = input("Brief note on what happened today: ")
    except (KeyboardInterrupt, EOFError):
        print("\nEntry cancelled. Nothing was saved.")
        return

    entry = Entry.from_inputs(importance, actions, discomfort, note)

    overwrite = False
    if storage.has_entry_for(entry.date):
        try:
            resp = input(f"\nAn entry already exists for {entry.date}. Overwrite? (y/n): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nEntry cancelled. Nothing was saved.")
            return
        if resp != "y":
            print("Entry not saved.")
            return
        overwrite = True

    level = DissonanceLevel.from_score(entry.dissonance)
    print(f"\n--- Today's Result ---")
    print(f"Cognitive Dissonance Score: {entry.dissonance:.1f}/10")
    print(level.message)

    storage.save(entry, overwrite=overwrite)
    print(f"Progress saved to '{storage.path}'.")


def rolling_average(values: list[float], window: int = 7) -> list[float]:
    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        result.append(mean(values[start : i + 1]))
    return result


def longest_high_streak(entries: list[Entry], threshold: float = HIGH_DISSONANCE_THRESHOLD) -> int:
    """Longest run of consecutive entries at/above the high-dissonance threshold."""
    longest = current = 0
    for e in entries:
        if e.dissonance >= threshold:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def generate_chart(storage: DissonanceStorage, plot_path: Path = DEFAULT_PLOT_FILE) -> None:
    entries = storage.load_entries()
    if not entries:
        print("\nNo data recorded yet. Record a few days first!")
        return

    entries.sort(key=lambda e: e.date)
    dates = [e.date for e in entries]
    dissonance_scores = [e.dissonance for e in entries]
    discomfort_scores = [e.discomfort for e in entries]
    trend = rolling_average(dissonance_scores, window=7)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, dissonance_scores, marker='o', color='#e74c3c', linewidth=1.5,
              alpha=0.6, label='Daily Dissonance')
    plt.plot(dates, discomfort_scores, marker='x', linestyle='--', color='#3498db',
              alpha=0.5, label='Reported Discomfort')
    plt.plot(dates, trend, color='#c0392b', linewidth=2.5, label='7-Day Moving Average (Trend)')

    plt.title('Cognitive Dissonance Trend', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=11, labelpad=10)
    plt.ylabel('Score (1-10)', fontsize=11)
    plt.ylim(0, 10.5)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    print(f"\nChart updated and saved as '{plot_path}'!")

    print("\n--- Summary ---")
    print(f"Total entries: {len(entries)}")
    print(f"Average dissonance: {mean(dissonance_scores):.1f}/10")
    best = min(entries, key=lambda e: e.dissonance)
    worst = max(entries, key=lambda e: e.dissonance)
    print(f"Best day: {best.date} ({best.dissonance:.1f}/10)")
    print(f"Worst day: {worst.date} ({worst.dissonance:.1f}/10)")
    streak = longest_high_streak(entries)
    if streak >= 3:
        print(f"⚠ Longest high-dissonance streak: {streak} consecutive days.")

    # Headless-safe display: don't crash if there's no GUI backend available
    try:
        if matplotlib.get_backend().lower() != "agg":
            plt.show()
    except Exception:
        pass
    finally:
        plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Daily Cognitive Dissonance Tracker")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_FILE,
                        help=f"Path to the CSV data file (default: {DEFAULT_DATA_FILE})")
    parser.add_argument("--plot", type=Path, default=DEFAULT_PLOT_FILE,
                        help=f"Path to save the trend chart (default: {DEFAULT_PLOT_FILE})")
    # parse_known_args ignores extra args injected by Jupyter/Colab
    # (e.g. "-f /root/.../kernel-xxxx.json") instead of crashing on them.
    args, _unknown = parser.parse_known_args()
    return args


def main() -> None:
    args = parse_args()
    storage = DissonanceStorage(path=args.data)

    while True:
        print("\n==============================")
        print("  COGNITIVE DISSONANCE TRACKER")
        print("==============================")
        print("1. Record today's entry")
        print("2. Generate trend chart")
        print("3. Exit")
        try:
            choice = input("Choose an option (1-3): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if choice == "1":
            record_entry(storage)
        elif choice == "2":
            generate_chart(storage, plot_path=args.plot)
        elif choice == "3":
            print("Keep aligning your actions with your values. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
