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


## 🩺 For Therapists & Non-Technical Users (No Setup Required)

If you do not know how to code, you do not need to download or install anything on your computer. You can run the assessment script directly inside your web browser via **Google Colab** in under 60 seconds:

1. **Open the Assessment Script:** Open the `narcissism_assessment.py` file inside this GitHub repository and copy all the text inside it.
2. **Launch Google Colab:** Click here to open [Google Colab](https://colab.research.google.com/) (a free, secure tool by Google that runs code in your browser). Sign in with any Google account.
3. **Create a New Sheet:** Click on **"New Notebook"** (or *Nuevo cuaderno*) at the bottom of the pop-up window.
4. **Paste and Play:** Click inside the empty gray box that appears, paste the code you copied, and click the small **Play Button (▶️)** on the left side of the box.

The script will instantly launch an interactive questionnaire right on your screen. Type in your ratings (from 0 to 3) for the patient, hit enter after each, and it will generate a clean psychological summary matrix for your clinical notes!

## 🛠️ How to Run the Simulation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/davidstocco2024-cell/python-for-psychology.git
    cd python-for-psychology
