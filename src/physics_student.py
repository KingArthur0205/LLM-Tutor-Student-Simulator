import anthropic
import utils

from dataclasses import dataclass
from typing import List

@dataclass
class StudentProfile:
    knowledge_level: int  # 1-5
    engagement_style: str  # curious, reserved, interactive, challengeSeeking
    misconceptions: List[str]
    confidence: str  # low, medium, high
    expressiveness: str  # minimal, moderate, detailed
    pacing: str  # slow, moderate, quick

class PhysicsStudentSimulator:
    def __init__(self, api_key: str):
        # Model parameters
        self.model = "claude-3-5-sonnet-20241022" # Latest model as of 2024-11-21
        self.temperature = 0
        self.max_token = 1000

        self.client = anthropic.Client(api_key=api_key)
        self.base_prompt = utils.student_system_prompt
        self.conversation_history = [{"role": "system", "content": self.base_prompt}]
        
    
    # Converts a student class to string to feed into the LLM
    def create_profile_xml(self, profile: StudentProfile) -> str:
        """Convert student profile to XML format."""
        return f"""
        <currentProfile>
            <knowledgeLevel>{profile.knowledge_level}</knowledgeLevel>
            <engagementStyle>{profile.engagement_style}</engagementStyle>
            <misconceptions>
                {chr(10).join([f'- {m}' for m in profile.misconceptions])}
            </misconceptions>
            <personalityTraits>
                <confidence>{profile.confidence}</confidence>
                <expressiveness>{profile.expressiveness}</expressiveness>
                <pacing>{profile.pacing}</pacing>
            </personalityTraits>
        </currentProfile>
        """

    def generate_response(self, 
                         profile: StudentProfile, 
                         physics_problem: str,
                         tutor_question: str) -> str:
        """Generate a student response to a physics problem or tutor question."""
        
        # Construct the complete prompt
        profile_xml = self.create_profile_xml(profile)
        self.conversation_history.append({"role":"user", "content": tutor_question})

        prompt = f"""
        Student:
        {profile_xml}

        Physics Problem:
        {physics_problem}

        {self.conversation_history}

        Tutor's Question:
        {tutor_question}

        Generate a student response that matches the profile configuration defined above.
        """

        # Call Claude API
        response = self.client.messages.create(
            model=self.model, 
            max_tokens=self.max_token,
            temperature=self.temperature,
            system=self.base_prompt,
            messages=[{"role": "user", "content": prompt}]
        )

        self.conversation_history.append({"role": "assistant", "content": response})
        
        return f"{response.content[0].text}"