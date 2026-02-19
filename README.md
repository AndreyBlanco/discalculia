# Overview

NumWorld — Aventura Numerica is an educational game built with Python and the
Arcade library, designed as a playful observation tool to help educators identify
possible early indicators of dyscalculia in young children.

The game features 5 levels, each focused on a fundamental numerical skill:

1. **Subitizing** — Recognizing quantities at a glance
2. **Counting** — Counting objects with precision
3. **Magnitude Comparison** — Identifying which group has more
4. **Estimation** — Approximating large quantities
5. **Number Sequencing** — Ordering numbers from least to greatest

While the child plays, the system discreetly records performance data (accuracy,
response time, error patterns) and generates an observational summary for the
educator at the end of the session.

**Important:** This is an OBSERVATION tool, NOT a diagnostic instrument. Results
should be interpreted by a qualified professional in the context of a complete
evaluation.

Together with my wife, a special education teacher, I have designed several
educational board games. My purpose for writing this software was to take the
first step in bringing that passion into the digital world by learning how to
create interactive tools using a Python game framework. This project represents
the natural evolution from physical board games to digital educational tools that
can support educators in their work.

The game meets the following requirements:
- **Graphics:** Gem-shaped objects drawn with geometric primitives, animated panels, buttons, and progress bars.
- **User Input:** All interactions are handled through mouse clicks, making it accessible for young players.
- **Moveable Objects:** Gems float with sinusoidal animations in all levels, and in Level 4 (Estimation) gems bounce around the screen.
- **Levels:** 5 distinct levels with different mechanics and increasing complexity, fulfilling the variable difficulty requirement.

[Software Demo Video] https://byupathwayworldwideprod-my.sharepoint.com/:v:/g/personal/ablancoalfaro_byupathway_edu/IQDSiwSO6dCeRL-zuP29wAVzAQqTYvad62jUcxYyVZUABJo?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=BnT4oc

# Development Environment

**Tools used:**
- Visual Studio Code as the primary IDE
- Python 3.11.9
- Git for version control
- Windows operating system

**Programming language and libraries:**
- **Python 3.11** — Main programming language
- **Arcade 2.6.17** — 2D game framework for Python, used for rendering graphics, handling user input, and managing the game loop
- **math** (standard library) — Mathematical functions for sinusoidal animations and geometric calculations
- **random** (standard library) — Random number generation for level content and gem placement
- **time** (standard library) — Tracking response times for the observational report
- **json** (standard library) — Serializing the observational report to a file

To install and run the project:

    pip install arcade==2.6.17
    python main.py

# Useful Websites

* [Arcade Academy - Official Documentation](https://api.arcade.academy/en/2.6.17/)
* [Arcade Academy - Example Code](https://api.arcade.academy/en/2.6.17/examples/index.html)
* [Python Arcade Tutorial - Real Python](https://realpython.com/arcade-python-game-framework/)
* [Arcade Views and Screens Tutorial](https://api.arcade.academy/en/2.6.17/tutorials/views/index.html)
* [Python Official Documentation - math module](https://docs.python.org/3/library/math.html)
* [Stack Overflow - Python Arcade Tag](https://stackoverflow.com/questions/tagged/python-arcade)

# Future Work

* Add sound effects for correct/incorrect answers and background music for each level to enhance engagement
* Replace geometric primitives with animated sprite images of gems and animals for a more visually appealing experience
* Implement a save/load system so players can resume their progress in a future session
* Add more levels covering additional skills such as basic operations (addition/subtraction), pattern recognition, and one-to-one correspondence
* Create an educator dashboard where teachers can view reports from multiple students, compare results, and track progress over time
* Improve accessibility by adding colorblind-friendly palettes, adjustable font sizes, and screen reader compatibility
* Migrate data storage from JSON files to a SQLite database for managing multiple sessions and students
* Explore a web-based version using Pyodide or similar technology to allow access without installation