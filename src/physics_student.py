import anthropic
import utils
import itertools
import random

from dataclasses import dataclass
from typing import List

@dataclass
class StudentProfile:
    knowledge_level: str  = None # 1-5
    engagement_style: str = None # curious, reserved, interactive, challengeSeeking
    misconceptions: List[str] = None
    confidence: str  = None# low, medium, high
    expressiveness: str  = None# minimal, moderate, detailed
    pacing: str  = None# slow, moderate, quick
    traits: str = None

    def __str__(self):
        # Format the string as desired
        return f"{self.knowledge_level}_{self.engagement_style}_{self.confidence}_{self.expressiveness}_{self.pacing}"

class PhysicsStudentSimulator:
    def __init__(self, api_key: str, student_profile: StudentProfile, physics_problem: str, if_simplified: bool = False):
        # Model parameters
        self.model = "claude-3-5-haiku-20241022" # Latest model as of 2024-11-21
        self.temperature = 0
        self.max_token = 1000

        self.client = anthropic.Client(api_key=api_key)
        self.base_prompt = utils.student_system_prompt if not if_simplified else utils.simplified_system_prompt
        self.conversation_history = [{"role": "system", "content": self.base_prompt}]
        self.profile = student_profile
        self.physics_problem = physics_problem
        self.if_simplified = if_simplified
        
    
    # Converts a student class to string to feed into the LLM
    def create_profile_xml(self, profile: StudentProfile) -> str:
        if self.if_simplified:
            return f"""
                <studentConfig>
                    <knowledgeLevel>{profile.knowledge_level}</knowledgeLevel>
                    <engagementStyle>{profile.engagement_style}</engagementStyle>
                    <traits>{profile.traits}</traits>
                </studentConfig>
            """
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

    def generate_response(self, tutor_question: str) -> str:
        """Generate a student response to a physics problem or tutor question."""
        
        # Construct the complete prompt
        profile_xml = self.create_profile_xml(self.profile)
        self.conversation_history.append({"role":"user", "content": tutor_question})

        prompt = f"""
        Student:
        {profile_xml}

        Physics Problem:
        {self.physics_problem}

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
    
def style_generate(style, styles):
    return str(style) + "-" + styles[style]

def profile_gen():
    combinations = list(itertools.product(
        utils.student_engagement_styles.items(),
        utils.student_knowledge_levels.items(),
        utils.student_expressiveness_levels.items(),
        utils.student_pacing_styles.items(),
        utils.student_confidence_levels.items()
    ))
    
    (
        (eng_level, eng_desc),
        (k_level, k_desc),
        (exp_level, exp_desc),
        (pac_level, pac_desc),
        (conf_level, conf_desc)
    ) = random.choice(combinations)

    return StudentProfile(
            knowledge_level=style_generate(k_level, utils.student_knowledge_levels),
            engagement_style=style_generate(eng_level, utils.student_engagement_styles),
            misconceptions=[
                "Confusing static equilibrium"
            ],
            confidence=style_generate(conf_level, utils.student_confidence_levels),
            expressiveness=style_generate(exp_level, utils.student_expressiveness_levels),
            pacing=style_generate(pac_level, utils.student_pacing_styles)
        )

def simp_profile_gen(knowledge_level, engagement_style):
    return StudentProfile(
        knowledge_level=style_generate(knowledge_level, utils.student_knowledge_levels),
        engagement_style=style_generate(engagement_style, utils.student_engagement_styles),
        traits=style_generate(engagement_style, utils.student_traits))
