# Psychological Profile Modeling via OOP (Python)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An educational object-oriented framework for simulating and analyzing complex psychological profiles and behavioral patterns. Designed for students, researchers, and enthusiasts interested in the intersection of psychology and computational modeling.

## 🧠 Features

- **Object-Oriented Design:** Uses inheritance and polymorphism to model diverse profiles from a base `PsychologicalProfile` class.
- **Behavioral Simulation:** Simulates dynamic cycles like the Narcissistic Cycle (Love Bombing, Devaluation, Discard, Rage).
- **Trigger-Response Logic:** Profiles react differently to specific stimuli (e.g., criticism, praise, rejection).
- **Extensible Framework:** Ready for you to add your own profiles (e.g., Borderline, Avoidant, Schizoid).

## 🚀 Available Profiles

| Profile | Module | Key Traits Modeled | Behavioral Cycles |
| :--- | :--- | :--- | :--- |
| **Narcissistic** | `models/narcissism.py` | Grandiosity, Lack of Empathy, Need for Admiration | Love Bombing, Devaluation, Discard, Narcissistic Rage (DARVO) |
| *Avoidant* (Coming Soon) | `models/avoidant.py` | Social Inhibition, Fear of Rejection, Feelings of Inadequacy | Withdrawal, Avoidance of Intimacy |
| *Borderline* (Coming Soon) | `models/borderline.py` | Emotional Instability, Splitting, Fear of Abandonment | Idealization, Devaluation, Impulsive Actions |

## 🛠️ How to Run the Simulation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/davidstocco2024-cell/python-for-psychology.git
    cd python-for-psychology
