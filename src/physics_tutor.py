import utils
from openai import OpenAI

class PhysicsTutorSimulator:
    def __init__(self, api_key):
        self.model = "gpt-4-turbo"
        self.temperature = 0
        self.max_tokens = 1000
        self.client = OpenAI(api_key=api_key)
        self.base_prompt = utils.tutor_system_prompt
        self.conversation_history = [{"role": "system", "content": self.base_prompt}]

    def generate_response(self, student_response):
        # Append the user's message to the conversation history
        self.conversation_history.append({"role": "user", "content": student_response})
        
        # Make the API call with the updated conversation history
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # Create a history
        assistant_response = completion.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    
    def get_conversation_history(self):
        return self.conversation_history