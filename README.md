# STEM Tutor for Effective Problem-Solving
The STEM Tutor for Effective Problem-Solving is an AI-powered educational tool designed to guide students through structured problem-solving in STEM subjects.

## Project Menu
 - [src/main.py](https://github.com/KingArthur0205/LLM-Tutor-Student-Simulator/blob/main/src/main.py): Define the main workflow of the project
 - [src/utils.py](https://github.com/KingArthur0205/LLM-Tutor-Student-Simulator/blob/main/src/utils.py): Contains prompt definitions and various utility functions to support the simulator.
 - [src/physics_student.py](https://github.com/KingArthur0205/LLM-Tutor-Student-Simulator/blob/main/src/physics_student.py): Defines the student simulator based on Claude-3.5-Sonnet. It utilizes the StudentProfile class to simulate the student's behavior.
 - [src/physics_tutor.py](https://github.com/KingArthur0205/LLM-Tutor-Student-Simulator/blob/main/src/physics_tutor.py): Defines the tutor simulator powered by GPT-4-Turbo.
 - [src/gpt_evaluator.py](https://github.com/KingArthur0205/LLM-Tutor-Student-Simulator/blob/main/src/gpt_evaluator.py): Implements the GPT-4-Turbo-based LLMScore calculator, which evaluates and compares student and tutor responses against a predefined set of required materials.