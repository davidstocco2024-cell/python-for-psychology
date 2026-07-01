# -*- coding: utf-8 -*-
"""
Educational Behavioral Cycle Simulation
------------------------------------------------
IMPORTANT: This module simulates a fictional profile ("Subject Alpha")
reacting to events, purely to demonstrate OOP concepts (state,
encapsulation, inheritance). It does not model, diagnose, or
characterize any real person. Concepts like "narcissistic injury" or
"DARVO" are simplified for teaching purposes and are not a substitute
for clinical literature or a licensed professional's assessment.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod


DISCLAIMER = (
    "Educational simulation only -- not a model of any real individual."
)


class Subtype(Enum):
    GRANDIOSE = "grandiose"
    VULNERABLE = "vulnerable"


class RelationshipStage(Enum):
    LOVE_BOMBING = "love_bombing"
    DEVALUATION = "devaluation"
    DISCARD = "discard"


@dataclass
class SimulationEvent:
    """A single structured event emitted by the simulation.

    Kept as data (not a print statement) so it can be logged,
    collected into a list, exported to CSV, or analyzed later
    (e.g. loaded into Tableau or queried from SQL Server) instead
    of being locked inside console output.
    """
    subject: str
    event_type: str
    detail: str
    supply_level: float
    ego_inflation: float
    empathy_level: float


class PsychologicalProfile(ABC):
    """Shared base for any simulated profile in this repo."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def summary(self) -> dict:
        """Return the current state as a plain dict."""
        raise NotImplementedError


class NarcissisticProfile(PsychologicalProfile):
    """
    Simulates a fictional profile's reaction to praise, criticism, and
    relationship-cycle events. All weights below are arbitrary
    teaching constants, not derived from any validated model.
    """

    # Named constants instead of magic numbers
    PRAISE_EGO_WEIGHT = 0.1
    CRITICISM_SUPPLY_DROP = 4.0
    DEVALUATION_EMPATHY_DROP = 0.5
    STARTING_EGO_INFLATION = 9.5
    STARTING_EMPATHY = 1.0
    STARTING_NEED_FOR_ADMIRATION = 10.0
    STARTING_SUPPLY = 5.0

    def __init__(self, name: str, subtype: Subtype = Subtype.GRANDIOSE):
        super().__init__(name)
        self.subtype = subtype
        self.ego_inflation = self.STARTING_EGO_INFLATION
        self.empathy_level = self.STARTING_EMPATHY
        self.need_for_admiration = self.STARTING_NEED_FOR_ADMIRATION
        self.narcissistic_supply_reservoir = self.STARTING_SUPPLY
        self.fragile_self_esteem = True

        self.event_log: list[SimulationEvent] = []

    def _log(self, event_type: str, detail: str) -> SimulationEvent:
        event = SimulationEvent(
            subject=self.name,
            event_type=event_type,
            detail=detail,
            supply_level=round(self.narcissistic_supply_reservoir, 1),
            ego_inflation=round(self.ego_inflation, 1),
            empathy_level=round(self.empathy_level, 1),
        )
        self.event_log.append(event)
        return event

    def receive_praise(self, intensity: float) -> SimulationEvent:
        """Simulates receiving praise, which increases narcissistic supply."""
        self.narcissistic_supply_reservoir = min(
            10.0, self.narcissistic_supply_reservoir + intensity
        )
        self.ego_inflation = min(
            10.0, self.ego_inflation + (intensity * self.PRAISE_EGO_WEIGHT)
        )
        return self._log("praise_received", f"Supply and ego increased by intensity {intensity}")

    def experience_criticism(self) -> SimulationEvent:
        """
        Simulates a reaction to criticism, which can trigger a defensive
        response if fragile_self_esteem is set.
        """
        self.narcissistic_supply_reservoir = max(
            0.0, self.narcissistic_supply_reservoir - self.CRITICISM_SUPPLY_DROP
        )
        if self.fragile_self_esteem:
            return self._trigger_defensive_response()
        return self._log("criticism_received", "No defensive response triggered")

    def _trigger_defensive_response(self) -> SimulationEvent:
        """Internal defense-mechanism reaction, driven by subtype."""
        if self.subtype == Subtype.GRANDIOSE:
            detail = "Deny-Attack-Reverse (DARVO) style response"
        else:
            detail = "Victim-framing response"
        return self._log("defensive_response", detail)

    def interact_with_target(self, stage: RelationshipStage) -> SimulationEvent:
        """Models one stage of a cyclic relationship pattern."""
        if stage == RelationshipStage.LOVE_BOMBING:
            detail = "Excessive affection directed at target"
        elif stage == RelationshipStage.DEVALUATION:
            self.empathy_level = max(0.0, self.empathy_level - self.DEVALUATION_EMPATHY_DROP)
            detail = "Hyper-criticism / undermining directed at target"
        else:  # DISCARD
            detail = "Abrupt withdrawal from target"
        return self._log(f"relationship_{stage.value}", detail)

    def summary(self) -> dict:
        return {
            "name": self.name,
            "subtype": self.subtype.value,
            "ego_inflation": round(self.ego_inflation, 1),
            "empathy_level": round(self.empathy_level, 1),
            "need_for_admiration": round(self.need_for_admiration, 1),
            "narcissistic_supply_reservoir": round(self.narcissistic_supply_reservoir, 1),
        }

    def export_event_log(self) -> list[dict]:
        """Returns the event log as a list of dicts -- ready for
        json.dump(), pandas.DataFrame(), or writing to CSV for
        downstream analysis (e.g. in Tableau)."""
        return [asdict(event) for event in self.event_log]


# --- Simulation Example ---
if __name__ == "__main__":
    print(DISCLAIMER, "\n")

    profile = NarcissisticProfile(name="Subject Alpha", subtype=Subtype.GRANDIOSE)

    events = [
        profile.receive_praise(intensity=3.5),
        profile.interact_with_target(RelationshipStage.LOVE_BOMBING),
        profile.interact_with_target(RelationshipStage.DEVALUATION),
        profile.experience_criticism(),
    ]

    for e in events:
        print(f"[{e.event_type}] {e.detail}  "
              f"(supply={e.supply_level}, ego={e.ego_inflation}, empathy={e.empathy_level})")

    print("\nFinal state:", profile.summary())
