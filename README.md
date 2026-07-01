# Psychological Trait Modeling via OOP (Python)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An educational object-oriented framework for exploring how psychological *concepts* — traits, behavioral cycles, trigger-response patterns — can be modeled in code. Built for students, self-taught programmers, and anyone interested in the intersection of OOP design and psychology as a **teaching tool**, not a clinical one.

> ⚠️ **This is not a diagnostic or assessment instrument.** The scoring in this repo is illustrative only, written for practicing inheritance, polymorphism, and encapsulation in Python. It has no psychometric validation (no reliability testing, no normative sample) and must never be used to label, screen, or diagnose a real person. Real personality assessment requires a validated instrument (e.g. NPI-16, PID-5) and a structured clinical interview conducted by a licensed professional, per DSM-5 criteria.

## 🧠 Features

- **Object-Oriented Design:** Uses inheritance and polymorphism to model different trait profiles from a shared `PsychologicalProfile` base class.
- **Behavioral Simulation:** Demonstrates how a coded "cycle" (e.g. idealization → devaluation → discard) can be represented as class state transitions.
- **Trigger-Response Logic:** Profiles react differently to sample stimuli (e.g. criticism, praise, rejection) — a practical example of polymorphic method behavior.
- **Extensible Framework:** Structured so you can add new profile subclasses (e.g. Avoidant, Borderline) by implementing one method.

## 🚀 Available Profiles

| Profile | Module | Concepts Modeled | Simulated Cycle |
| :--- | :--- | :--- | :--- |
| **Narcissistic (demo)** | `models/narcissism.py` | Grandiosity, empathy trade-off, need for validation | Idealization → Devaluation → Discard |
| *Avoidant* (Coming Soon) | `models/avoidant.py` | Social inhibition, fear of rejection | Withdrawal patterns |
| *Borderline* (Coming Soon) | `models/borderline.py` | Emotional volatility, splitting | Idealization / devaluation swings |

All "profiles" here are simplified teaching abstractions of concepts discussed in clinical psychology literature — not implementations of any clinical criteria.

## 🎓 Who This Is For

This repo is aimed at **learners**, not practitioners:

- CS/Python students practicing OOP through a domain that isn't another `Animal`/`Dog`/`Cat` example
- Psychology students curious about how trait models could be represented computationally
- Anyone in a study group wanting a discussion piece on the limits of turning qualitative human behavior into code

It is **not** intended for use by therapists on clients, for self-diagnosis, or for any real assessment purpose. If you're a mental health professional and want to explore ideas around measurement-based care, please refer to peer-reviewed, validated instruments and your governing clinical body's guidelines instead.

## ▶️ Try It in Your Browser (No Setup Required)

You can run the demo script without installing anything, using **Google Colab**:

1. **Open the script:** Open `narcissism_demo.py` in this repo and copy its contents.
2. **Launch Google Colab:** Go to [Google Colab](https://colab.research.google.com/) and sign in with any Google account.
3. **New Notebook:** Click **"New Notebook"**.
4. **Paste and run:** Paste the code into a cell and click the **▶️ Play** button.

The script walks through a short self-reflection questionnaire (rate each item 0–3) and prints a summary of the modeled trait dimensions — for exploring the code's behavior, not for evaluating a real person.

## 🛠️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/davidstocco2024-cell/python-for-psychology.git
   cd python-for-psychology
   ```

2. **Run the demo:**
   ```bash
   python narcissism_demo.py
   ```

## 🧩 Extending the Framework

Each profile follows the same contract: subclass `PsychologicalProfile` and implement `_compute_dimensions()`, which turns raw input into a list of `TraitDimension` objects. To add a new profile:

```python
class AvoidantTraitProfile(PsychologicalProfile):
    def _compute_dimensions(self) -> list[TraitDimension]:
        # your scoring logic here
        ...
```

Pull requests adding new demo profiles, tests, or documentation are welcome.

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
