import os
import xml.etree.ElementTree as ET
import utils

from dotenv import load_dotenv, find_dotenv
from physics_student import PhysicsStudentSimulator, profile_gen
from gpt_evaluator import GPTEvaluator, generate_log_row
from physics_tutor import PhysicsTutorSimulator

def create_LLM_agents(profile):
    claude_student_simulator = PhysicsStudentSimulator(os.environ.get("ANTHROPIC_API_KEY"), profile, utils.physics_problem)
    gpt_tutor_simulator = PhysicsTutorSimulator(os.environ.get("OPENAI_API_KEY"))
    gpt_evaluator = GPTEvaluator(os.environ.get("OPENAI_API_KEY"))
    return claude_student_simulator, gpt_tutor_simulator, gpt_evaluator

def main():
    # Load enviornment for LLM APIs
    _ = load_dotenv(find_dotenv())
    # Randomly create a student profile from sample space
    profile = profile_gen()

    # Create Student, Tutor, LLMScore evaluator
    claude_student_simulator, gpt_tutor_simulator, gpt_evaluator = create_LLM_agents(profile)

    student_response = "Can you help me with this question?"
    print(f"Student: {student_response}\n")

    conversation_counter = 0
    tutor_response_len = 0
    student_response_len = 0
    try:
        while True:
            tutor_response = gpt_tutor_simulator.generate_response(student_response=student_response)
            # Generate student response
            student_response = claude_student_simulator.generate_response(tutor_question=tutor_response)
                
            print("Tutor response: ", tutor_response, "\n")
            print("Student Response:", student_response)

            if not utils.execution_control():
                print("Exiting loop...")
                break
            conversation_counter += 1
            tutor_response_len += len(tutor_response)
            student_response_len += len(student_response)
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user")

    student_response = claude_student_simulator.generate_response(tutor_question="Can you provide a concise summary of the key knowledge and insights you've gained so far to demonstrate your understanding and progress in this study?")
    row = generate_log_row(profile,gpt_evaluator, gpt_tutor_simulator.get_conversation_history(), tutor_response, student_response, conversation_counter, tutor_response_len, student_response_len)
    utils.write_data(row) # Record the data into a csv file in the data directory

if __name__ == "__main__":
    main()
