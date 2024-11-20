import utils
from openai import OpenAI

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