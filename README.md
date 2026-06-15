# theory-of-behavior
A Fundamental Comprehensive Algorithm for Human Behavior — formal behavioral decision algorithm with Python implementation.
The Theory of Behavior -
A Fundamental Comprehensive Algorithm for Human Behavior.
D.M. Chabon — Applied Behavioral Science Strategies

## 🚀 Live Interactive Walkthrough
**Run the algorithm in your browser — no installation required:**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mkdBS-rsPmBlGhUM2i94LhsQk4DK8iCC?usp=sharing)

Overview
This repository contains the Python implementation of The Theory of Behavior — a formally specified, invariant algorithm modeling how people reach behavioral decisions.
The algorithm treats behavioral options as sets of perceived, value-laden attributes computed from three factors:

Rank (K) — the relative importance of each attribute (0-10)
Saturation (S) — proximity to optimal level (0-1)
Contingency (C) — perceived probability of occurrence (0-1)

The model is invariant across all individuals regardless of physiological, genetic, or cultural variation. Individual differences manifest exclusively in the values of K, S, and C — not in the algorithm itself.

The Core Equation
V(aj) = C × (S × K)
B(Bi) = R(Bi) − P(Bi)
B*(Bi) = D × B(Bi)
Where:

V = attribute valence
R = sum of reward attribute valences
P = sum of punishment attribute valences
B = behavioral option value
B* = salience-adjusted behavioral option value
D = decision salience from the individual's umwelt (0-1)

The enacted behavior is the option with the highest B* value.

Running the Code
No external libraries required. Standard Python 3.x.
Online — no installation needed:
Go to online-python.com, paste the code, click Run.
Local installation:
bashpython theory_of_behavior.py

What the Code Demonstrates

Full attribute valence computation for each behavioral option
Reward and punishment attribute handling
Salience adjustment via D from the individual's umwelt
Behavioral selection with conflict detection
Bayesian updating across K, S, and C modes
Sensitivity demonstration showing invariance in action


The Full Paper
The Theory of Behavior: A Fundamental Comprehensive Algorithm for Human Behavior
Available on SSRN: https://ssrn.com/abstract=6242578
Zenodo DOI: https://doi.org/10.5281/zenodo.20069418
ORCID: https://orcid.org/0009-0008-2557-1009

License
Copyright © 2026 D.M. Chabon. All Rights Reserved.
This code is provided for research, evaluation, and educational purposes. Commercial use requires explicit written permission from the author.
