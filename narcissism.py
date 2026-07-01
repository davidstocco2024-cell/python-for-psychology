# -*- coding: utf-8 -*-
class NarcissisticProfile:
    """
    A class to model the psychological and behavioral patterns
    of a narcissistic personality profile for educational and analytical purposes.
    """

    def __init__(self, name: str, subtype: str = "Grandiose"):
        self.name = name
        self.subtype = subtype  # e.g., Grandiose, Vulnerable/Covert

        # Core psychological attributes (scaled 0 to 10)
        self.ego_inflation = 9.5
        self.empathy_level = 1.0
        self.need_for_admiration = 10.0

        # Internal state
        self.narcissistic_supply_reservoir = 5.0  # Fluctuates based on external validation
        self.fragile_self_esteem = True

    def receive_praise(self, intensity: float):
        """Simulates receiving praise, which increases narcissistic supply."""
        print(f"\n[Event] {self.name} received praise.")
        self.narcissistic_supply_reservoir = min(10.0, self.narcissistic_supply_reservoir + intensity)
        self.ego_inflation = min(10.0, self.ego_inflation + (intensity * 0.1))
        print(f"-> Supply increased to: {self.narcissistic_supply_reservoir}/10. Ego inflated.")

    def experience_criticism(self):
        """
        Simulates the reaction to criticism, often triggering 'narcissistic injury'
        due to underlying fragile self-esteem.
        """
        print(f"\n[Event] {self.name}'s ego was challenged or criticized.")
        self.narcissistic_supply_reservoir = max(0.0, self.narcissistic_supply_reservoir - 4.0)

        # Trigger defense mechanisms
        self._trigger_narcissistic_rage()

    def _trigger_narcissistic_rage(self):
        """An internal (private) method representing an automatic defense mechanism."""
        print(f"-> [CRITICAL] Narcissistic Injury Detected!")
        if self.subtype == "Grandiose":
            print(f"-> Behavior: {self.name} initiates DARVO (Deny, Attack, Reverse Victim & Offender).")
        elif self.subtype == "Vulnerable":
            print(f"-> Behavior: {self.name} adopts a severe victim mentality to weaponize guilt.")

    def interact_with_target(self, relationship_stage: str):
        """Models the cyclic nature of narcissistic relationships."""
        print(f"\n[Relationship Stage] {relationship_stage.upper()}")

        if relationship_stage.lower() == "love_bombing":
            print(f"-> Action: {self.name} showers the target with excessive affection to secure a source of supply.")
        elif relationship_stage.lower() == "devaluation":
            self.empathy_level = max(0.0, self.empathy_level - 0.5)
            print(f"-> Action: {self.name} begins subtle gaslighting and hyper-criticism to lower the target's self-esteem.")
        elif relationship_stage.lower() == "discard":
            print(f"-> Action: {self.name} abruptly cuts ties or emotionally abandons the target because supply is depleted.")


# --- Simulation Example ---
if __name__ == "__main__":
    # Instantiating the profile
    profile = NarcissisticProfile(name="Subject Alpha", subtype="Grandiose")

    # 1. The Cycle of Supply
    profile.receive_praise(intensity=3.5)

    # 2. Behavioral Patterns in Relationships
    profile.interact_with_target("love_bombing")
    profile.interact_with_target("devaluation")

    # 3. Narcissistic Injury
    profile.experience_criticism()

