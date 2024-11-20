import utils
from openai import OpenAI
from bert_score import score

class GPTEvaluator:
    def __init__(self, api_key: str):
        self.model = "gpt-4-turbo"
        self.temperature = 0
        self.max_tokens = 1000
        self.client = OpenAI(api_key=api_key)
        self.base_prompt = utils.LLM_evaluator_base_prompt
        self.conversation_history = [{"role": "system", "content": self.base_prompt}]
    
    def generate_response(self, tutor_summary):
        self.conversation_history.append({"role": "user", "content": utils.generate_LLM_evaluator_prompt(tutor_summary)})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # Create a history
        assistant_response = completion.choices[0].message.content
        return assistant_response
    
    def compute_llm_scores(self, response):
        llm_response = self.generate_response(response)
        return utils.extract_scores(llm_response)
    
def compute_bert_scores(response, prompt):
    p, r, fscore = score([response], [prompt], lang='en', verbose=True)
    return p.item(), r.item(), fscore.item()

def generate_log_row(profile, gpt_evaluator, chat_history, tutor_response, student_response, conversation_counter, tutor_response_len, student_response_len):
    # BERT scores
    bert_p, bert_r, bert_score = compute_bert_scores(tutor_response, utils.question_summary_prompt)
    student_bert_p, student_bert_r, student_bert_score = compute_bert_scores(student_response, utils.question_summary_prompt)

    # LLM scores
    llm_p, llm_r, llm_score = gpt_evaluator.compute_llm_scores(tutor_response)
    student_llm_p, student_llm_r, student_llm_score = gpt_evaluator.compute_llm_scores(student_response)

    # Prepare the row data
    return [
        str(profile),
        chat_history,
        tutor_response,
        student_response,
        profile.engagement_style,
        profile.knowledge_level,
        profile.expressiveness,
        profile.pacing,
        profile.confidence,
        conversation_counter,
        tutor_response_len // conversation_counter,
        student_response_len // conversation_counter,
        llm_p, llm_r, llm_score,
        bert_p, bert_r, bert_score,
        student_llm_p, student_llm_r, student_llm_score,
        student_bert_p, student_bert_r, student_bert_score
    ]