# Psychological Trait Modeling via OOP (Python)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An educational object-oriented framework for exploring how psychological *concepts* — traits, behavioral cycles, generational patterns — can be modeled in code. 

Built for students, self-taught programmers, and anyone interested in the intersection of OOP design and psychology as a **teaching tool**, not a clinical one.

> ⚠️ **This is not a diagnostic or assessment instrument.** Every scoring rule and multiplier in this repo is illustrative only, written for practicing inheritance, polymorphism, and encapsulation in Python. None of it has psychometric validation (no reliability testing, no normative sample) and it must never be used to label, screen, or diagnose a real person. Real personality or family-systems assessment requires a validated instrument (e.g. NPI-16, PID-5) and a structured clinical evaluation conducted by a licensed professional.

## 🧠 Features

- **Object-Oriented Design:** Uses inheritance, encapsulation, and polymorphism to model different psychological concepts from shared base classes.
- **Self-Reflection Scoring:** Demonstrates a simple weighted scoring model (`narcissism_assessment.py`) with retry-safe input handling.
- **Behavioral Simulation:** Shows how a coded "cycle" (e.g. idealization → devaluation → discard) can be represented as class state transitions (`narcissism.py`).
- **Generational Modeling:** Uses class inheritance as a deliberate pun on *trait* inheritance across a fictional family (`family_trait_simulation.py`).
- **Extensible Framework:** Each module follows the same pattern — a base class plus one method to override — so new modules are cheap to add.

## 🚀 Modules in This Repo

| File | What It Demonstrates | Concepts Modeled |
| :--- | :--- | :--- |
| `narcissism_assessment.py` | Base class + subclass scoring pattern, safe input loops | Self-focus, need for validation, empathy trade-off |
| `narcissism.py` | Stateful simulation reacting to events, structured event logging | Idealization → Devaluation → Discard cycle |
| `family_trait_simulation.py` | Class inheritance (`Patient` extends `Individual`) as a pun on generational trait inheritance | Fictional multigenerational trait/coping-style transmission |

All of these are **simplified teaching abstractions** loosely inspired by concepts discussed in psychology literature (e.g. Bowen Family Systems ideas for the generational module) — none of them are implementations of real clinical criteria, and none should be run on real people's data.

## 🎓 Who This Is For

This repo is aimed at **learners**, not practitioners:

- CS/Python students practicing OOP through a domain that isn't another `Animal`/`Dog`/`Cat` example
- Psychology students curious about how trait models could be represented computationally
- Study groups wanting a discussion piece on the limits (and risks) of turning qualitative human behavior into code

It is **not** intended for use by therapists on real clients, for self-diagnosis, or for any real assessment purpose. All example prompts in the code ask for **fictional** names and data. If you're a mental health professional interested in measurement-based care, please use peer-reviewed, validated instruments under your governing clinical body's guidelines instead.

## ▶️ Try It in Your Browser (No Setup Required)

You can run any of the scripts without installing anything, using **Google Colab**:

1. **Open a script:** Open one of the `.py` files in this repo (e.g. `narcissism_assessment.py`) and copy its contents.
2. **Launch Google Colab:** Go to [Google Colab](https://colab.research.google.com/) and sign in with any Google account.
3. **New Notebook:** Click **"New Notebook"**.
4. **Paste and run:** Paste the code into a cell and click the **▶️ Play** button.

Each script walks through a short interactive exercise with **fictional** data and prints a summary — for exploring the code's behavior, not for evaluating a real person.

## 🛠️ How to Run Locally

```bash
git clone https://github.com/davidstocco2024-cell/python-for-psychology.git
cd python-for-psychology
python narcissism_assessment.py
# or
python narcissism.py
# or
python family_trait_simulation.py
```

## 🧩 Extending the Framework

Each module follows the same OOP contract: a base class defines the shared behavior, and a subclass fills in specific data. For example, in `narcissism_assessment.py`:

```python
class PsychologicalProfile(ABC):
    @abstractmethod
    def _compute_dimensions(self) -> list[TraitDimension]:
        ...

class YourNewProfile(PsychologicalProfile):
    def _compute_dimensions(self) -> list[TraitDimension]:
        # your own illustrative scoring logic here
        ...
```

Contributions adding new teaching modules, tests, or documentation are welcome — as long as new modules keep the same safety disclaimer and use fictional example data.

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
