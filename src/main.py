import os
import xml.etree.ElementTree as ET
import utils
import itertools
import csv
import random

from dotenv import load_dotenv, find_dotenv
from bert_score import score
from physics_student import StudentProfile, PhysicsStudentSimulator
from gpt_evaluator import GPTEvaluator
from physics_tutor import PhysicsTutorSimulator

    
def style_generate(style, styles):
    return str(style) + "-" + styles[style]

csv_file_path = 'student_tutor_sim.csv'
headers = [
    'student_profile', 'chat_history', 'tutor_summary',
    'engagement_level', 'knowledge_level', 'expressiveness_level',
    'pacing_style', 'confidence_level', 'conversation_counter',
    'LLM_Precision', 'LLM_Recall','LLM_score', 
    'BERT_Precision', 'BERT_Recall', 'BERT_score'
]

def main():
    _ = load_dotenv(find_dotenv())
    csv_file = open(csv_file_path, mode='a', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)
    if os.path.exists(csv_file_path):
        writer.writerow(headers)

    combinations = list(itertools.product(
        utils.student_engagement_styles.items(),
        utils.student_knowledge_levels.items(),
        utils.student_expressiveness_levels.items(),
        utils.student_pacing_styles.items(),
        utils.student_confidence_levels.items()
    ))

    # Pick one random configuration
    (
        (eng_level, eng_desc),
        (k_level, k_desc),
        (exp_level, exp_desc),
        (pac_level, pac_desc),
        (conf_level, conf_desc)
    ) = random.choice(combinations)
        # Create student and tutor
    claude_student_simulator = PhysicsStudentSimulator(os.environ.get("ANTHROPIC_API_KEY"))
    gpt_tutor_simulator = PhysicsTutorSimulator(os.environ.get("OPENAI_API_KEY"))
    gpt_evaluator = GPTEvaluator(os.environ.get("OPENAI_API_KEY"))
        
        # Create a student profile
    profile = StudentProfile(
            knowledge_level=style_generate(k_level, utils.student_knowledge_levels),
            engagement_style=style_generate(eng_level, utils.student_engagement_styles),
            misconceptions=[
                "Confusing static equilibrium"
            ],
            confidence=style_generate(conf_level, utils.student_confidence_levels),
            expressiveness=style_generate(exp_level, utils.student_expressiveness_levels),
            pacing=style_generate(pac_level, utils.student_pacing_styles)
    )

    student_response = "Can you help me with this question?"
    print(f"Student: {student_response}\n")

    conversation_counter = 0
    tutor_responses = []
    student_responses = []
    try:
        while True:
            tutor_response = gpt_tutor_simulator.generate_response(student_response=student_response)
            conversation_counter += 1
                
            # Generate student response
            student_response = claude_student_simulator.generate_response(
                profile=profile,
                physics_problem=utils.physics_problem,
                tutor_question=tutor_response
            )
                
            print("Tutor response: ", tutor_response, "\n")
            print("Student Response:", student_response)

            user_input = input().lower()  # Convert to lowercase for case-insensitive comparison
            if user_input == "z":
                print("Exiting loop...")
                break
            elif user_input == "":
                continue
            else:
                print("Invalid input. Press Enter or 'z'")
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user")

    student_response = claude_student_simulator.generate_response(
                profile=profile,
                physics_problem=utils.physics_problem,
                tutor_question="Can you provide a concise summary of the key knowledge and insights you’ve gained so far to demonstrate your understanding and progress in this study?"
            )
        
    bert_p, bert_r, bert_score = score([tutor_response], [utils.question_summary_prompt], lang='en', verbose=True)
    student_bert_p, student_bert_r, student_bert_score = score([student_response], [utils.question_summary_prompt], lang='en', verbose=True)

    llm_score = gpt_evaluator.generate_response(tutor_response)
    llm_p, llm_r, llm_score = utils.extract_scores(llm_score)
    student_llm_score = gpt_evaluator.generate_response(student_response)
    student_llm_p, student_llm_r, student_llm_score = utils.extract_scores(student_llm_score)

    student_profile = f"{k_level}_{eng_level}_{conf_level}_{exp_level}_{pac_level}_1"

    chat_history = gpt_tutor_simulator.get_conversation_history()
    row = [
            student_profile, chat_history, tutor_response, 
            eng_level, 
            k_level,
            exp_level, 
            pac_level, 
            conf_level, conversation_counter, llm_p, llm_r, llm_score, bert_p.item(), bert_r.item(), bert_score.item(),
            student_llm_p, student_llm_r, student_llm_score, student_bert_p.item(), student_bert_r.item(), student_bert_score.item()
    ]
    writer.writerow(row)
    csv_file.close()

if __name__ == "__main__":
    main()
