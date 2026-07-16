"""
Educational Generational Trait Simulator (fictional families only)
--------------------------------------------------------------------
IMPORTANT: This is a teaching demo for OOP inheritance, built loosely
around ideas from Bowen Family Systems Theory (multigenerational
transmission, differentiation of self). It is NOT a validated
assessment tool. The "inherited anxiety" formula and conflict
multipliers below are arbitrary teaching constants with no clinical
basis -- do not enter data about real patients or real families.
Use invented names for a fictional family when running this.

OOP concept demonstrated: class inheritance (Patient extends
Individual) as a playful parallel to *generational* inheritance of
traits -- the pun is the point of the exercise.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


DISCLAIMER = (
    "Educational simulation with fictional data only -- "
    "not a real assessment of any actual person or family."
)


class CopingStyle(Enum):
    AVOIDANT = "Avoidant"
    ANXIOUS = "Anxious"
    SECURE = "Secure"
    AGGRESSIVE = "Aggressive"


class RelationshipDynamic(Enum):
    ENMESHED = "Enmeshed"
    ANXIOUS_AVOIDANT_TRAP = "Anxious-Avoidant Trap"
    DISTANT = "Distant"


# Named constants instead of magic numbers scattered in the logic
CONFLICT_MULTIPLIERS = {
    RelationshipDynamic.ENMESHED: 1.8,
    RelationshipDynamic.ANXIOUS_AVOIDANT_TRAP: 1.5,
    RelationshipDynamic.DISTANT: 0.8,
}
SPILLOVER_RATIO = 0.7  # fraction of conflict impact that reaches the patient
MAX_SCALE = 10.0


class Individual:
    """Represents any person in the fictional family network."""

    def __init__(self, name: str, generation: int, coping_style: CopingStyle, baseline_anxiety: float):
        self.name = name
        self.generation = generation  # 1 = grandparents, 2 = parents, 3 = focal person
        self.coping_style = coping_style
        self.baseline_anxiety = baseline_anxiety  # illustrative 0.0-10.0 scale
        self.current_stress = baseline_anxiety


class Patient(Individual):
    """A focal person in the simulation, generated from two Individuals.

    This is the actual inheritance demo: Patient extends Individual
    (a Python class hierarchy), while *also* computing its starting
    traits from its "parents" (a toy model of generational transmission).
    Both meanings of "inheritance" collide here on purpose.
    """

    def __init__(self, name: str, father: Individual, mother: Individual):
        inherited_anxiety = round((father.baseline_anxiety + mother.baseline_anxiety) / 2.0, 1)
        inherited_coping = (
            father.coping_style if father.baseline_anxiety > mother.baseline_anxiety
            else mother.coping_style
        )

        super().__init__(name=name, generation=3, coping_style=inherited_coping, baseline_anxiety=inherited_anxiety)
        self.father = father
        self.mother = mother

    def print_family_report(self) -> None:
        print("\n" + "=" * 55)
        print(f"  FICTIONAL FAMILY TRAIT MAP: {self.name}")
        print("=" * 55)
        print(f" Father line: {self.father.name} "
              f"(Coping: {self.father.coping_style.value}, Anxiety: {self.father.baseline_anxiety}/10)")
        print(f" Mother line: {self.mother.name} "
              f"(Coping: {self.mother.coping_style.value}, Anxiety: {self.mother.baseline_anxiety}/10)")
        print("-" * 55)
        print(f" -> Simulated starting anxiety: {self.baseline_anxiety}/10")
        print(f" -> Simulated coping pattern:   {self.coping_style.value}")
        print("=" * 55)
        print(DISCLAIMER + "\n")


@dataclass
class ConflictOutcome:
    dynamic: str
    impact_score: float
    patient_stress_delta: float
    patient_total_stress: float


class FamilyRelationship:
    """Models a dynamic link between two Individuals in the simulation."""

    def __init__(self, person_a: Individual, person_b: Individual, dynamic: RelationshipDynamic):
        self.person_a = person_a
        self.person_b = person_b
        self.dynamic = dynamic

    def trigger_conflict(self, severity: float, focal_patient: Patient) -> ConflictOutcome:
        """Simulates a conflict event and its modeled spillover onto the
        focal patient. Multipliers are illustrative teaching constants,
        not derived from any validated model."""
        multiplier = CONFLICT_MULTIPLIERS[self.dynamic]
        impact_score = round(severity * multiplier, 1)
        patient_delta = round(impact_score * SPILLOVER_RATIO, 1)

        focal_patient.current_stress = min(MAX_SCALE, focal_patient.current_stress + patient_delta)

        return ConflictOutcome(
            dynamic=self.dynamic.value,
            impact_score=impact_score,
            patient_stress_delta=patient_delta,
            patient_total_stress=focal_patient.current_stress,
        )


# ---------------------------------------------------------------------
# Input helpers (retry instead of crashing on bad input)
# ---------------------------------------------------------------------

def prompt_float(message: str, low: float, high: float) -> float:
    while True:
        raw = input(message).strip()
        try:
            value = float(raw)
        except ValueError:
            print(f"  Please enter a number between {low} and {high}.")
            continue
        if not low <= value <= high:
            print(f"  Value must be between {low} and {high}.")
            continue
        return value


def prompt_enum(message: str, enum_cls: type[Enum]) -> Enum:
    options = {str(i + 1): member for i, member in enumerate(enum_cls)}
    option_text = ", ".join(f"{k}={v.value}" for k, v in options.items())
    while True:
        choice = input(f"{message} ({option_text}): ").strip()
        if choice in options:
            return options[choice]
        print("  Invalid choice, try again.")


def build_individual(role: str, generation: int) -> Individual:
    print(f"\n--- {role.upper()} (fictional) ---")
    name = input(f"{role}'s fictional name/code: ").strip() or f"{role}-Unnamed"
    coping = prompt_enum(f"{role}'s coping style", CopingStyle)
    anxiety = prompt_float(f"{role}'s baseline anxiety (0.0-10.0): ", 0.0, 10.0)
    return Individual(name, generation=generation, coping_style=coping, baseline_anxiety=anxiety)


# ---------------------------------------------------------------------
# Simulation entry point
# ---------------------------------------------------------------------

def run_simulation() -> None:
    print("=" * 55)
    print("  FAMILY TRAIT SIMULATION (educational, fictional)")
    print("=" * 55)
    print(DISCLAIMER)
    print("Enter details for an INVENTED family -- do not use real people.\n")

    father = build_individual("Father", generation=2)
    mother = build_individual("Mother", generation=2)

    print("\n--- FOCAL CHARACTER ---")
    patient_name = input("Focal character's fictional name/code: ").strip() or "Unnamed"
    patient = Patient(name=patient_name, father=father, mother=mother)
    patient.print_family_report()

    print("--- RELATIONSHIP DYNAMIC ---")
    dynamic = prompt_enum("Choose the parents' relationship dynamic", RelationshipDynamic)
    severity = prompt_float("\nConflict severity to simulate (1.0-5.0): ", 1.0, 5.0)

    relationship = FamilyRelationship(father, mother, dynamic=dynamic)
    outcome = relationship.trigger_conflict(severity=severity, focal_patient=patient)

    print(f"\n[Simulated event] Conflict between {father.name} and {mother.name} "
          f"({outcome.dynamic})")
    print(f" -> Modeled spillover onto {patient.name}: +{outcome.patient_stress_delta}")
    print(f" -> {patient.name}'s total simulated stress: {outcome.patient_total_stress}/10")
    print(f"\n{DISCLAIMER}\n")


if __name__ == "__main__":
    run_simulation()

