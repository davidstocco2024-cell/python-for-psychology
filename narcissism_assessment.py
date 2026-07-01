"""
Educational Personality Trait Reflection Tool
------------------------------------------------
IMPORTANT: This is a teaching demo for OOP concepts (inheritance,
encapsulation, polymorphism). It is NOT a validated psychological
instrument and must never be used to diagnose, screen, or label a
real person with a personality disorder. Real assessment of NPD (or
any personality disorder) requires a validated tool (e.g. NPI-16,
PID-5) and a structured clinical interview administered and
interpreted by a licensed clinician, per DSM-5 criteria.

This script models ONE trait dimension as a simple example. The
scoring below is illustrative only -- it has no psychometric
validation (no reliability, no normative sample).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


DISCLAIMER = (
    "This tool is for educational / self-reflection purposes only.\n"
    "It is not a diagnostic instrument and produces no clinical conclusions."
)


@dataclass
class TraitDimension:
    """A single named trait score on a 0-10 scale."""
    label: str
    value: float


class PsychologicalProfile(ABC):
    """
    Base class for a trait-reflection profile.

    Subclasses implement _compute_dimensions() to turn a raw
    questionnaire score into a set of named TraitDimension objects.
    This is the shared contract every trait profile follows.
    """

    MAX_RAW_SCORE: float = 15.0  # override per subclass if needed

    def __init__(self, name: str, raw_score: float, tier_label: str):
        self.name = name
        self.raw_score = raw_score
        self.tier_label = tier_label
        self.dimensions: list[TraitDimension] = self._compute_dimensions()

    @abstractmethod
    def _compute_dimensions(self) -> list[TraitDimension]:
        """Return a list of TraitDimension derived from raw_score."""
        raise NotImplementedError

    def display_profile(self) -> None:
        print("\n" + "=" * 50)
        print(f" TRAIT REFLECTION SUMMARY: {self.name}")
        print("=" * 50)
        print(f"Category (informal): {self.tier_label} ({self.raw_score} pts)")
        for dim in self.dimensions:
            print(f"{dim.label:<22} {dim.value}/10")
        print("=" * 50)
        print(DISCLAIMER + "\n")


class NarcissisticTraitProfile(PsychologicalProfile):
    """
    Example subclass modeling self-reported grandiosity-related traits.
    Scale factor and weights are arbitrary teaching constants, not
    derived from any validated instrument.
    """

    EMPATHY_INVERSE_WEIGHT = 0.8

    def _compute_dimensions(self) -> list[TraitDimension]:
        scale_factor = min(10.0, (self.raw_score / self.MAX_RAW_SCORE) * 10)
        empathy = round(10.0 - (scale_factor * self.EMPATHY_INVERSE_WEIGHT), 1)
        return [
            TraitDimension("Self-focus (self-rated)", round(scale_factor, 1)),
            TraitDimension("Need for validation", round(scale_factor, 1)),
            TraitDimension("Reported empathy", max(0.0, empathy)),
        ]


QUESTIONS = [
    "Tends to see own achievements/qualities as especially important",
    "Finds it hard to recognize or prioritize others' feelings",
    "Expects favorable treatment compared to others",
    "Has a strong need for admiration or validation from others",
    "Willing to use others to get what they want",
]

TIER_THRESHOLDS = [
    (4, "Low trait expression"),
    (8, "Moderate trait expression"),
    (12, "Elevated trait expression"),
]
DEFAULT_TIER = "High trait expression (self-reported)"


def get_rated_input(prompt: str) -> float:
    """Ask for a 0-3 rating, re-prompting on invalid input instead of
    aborting the whole session."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a number between 0 and 3.")
            continue
        if not 0 <= value <= 3:
            print("  Value must be between 0 and 3.")
            continue
        return value


def classify_tier(total_score: float) -> str:
    for threshold, label in TIER_THRESHOLDS:
        if total_score <= threshold:
            return label
    return DEFAULT_TIER


def run_self_reflection() -> NarcissisticTraitProfile:
    print("=" * 50)
    print("  SELF-REFLECTION EXERCISE (Educational demo)")
    print("=" * 50)
    print(DISCLAIMER)
    print("\nRate each statement from 0 (not at all) to 3 (very much):\n")

    respondent = input("Name or identifier (can be anonymous): ").strip() or "Anonymous"

    total_score = 0.0
    for i, question in enumerate(QUESTIONS, start=1):
        total_score += get_rated_input(f"{i}. {question} (0-3): ")

    tier = classify_tier(total_score)
    return NarcissisticTraitProfile(respondent, total_score, tier)


if __name__ == "__main__":
    profile = run_self_reflection()
    profile.display_profile()
