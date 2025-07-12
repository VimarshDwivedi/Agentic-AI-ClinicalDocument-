# from llm_setup import get_llm
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# class DialogueAgent:
#     def __init__(self, clinician_specialty: str = "general"):
#         self.clinician_specialty = clinician_specialty
#         self.llm = get_llm()
#         self.template = PromptTemplate.from_template("""
#         As a {specialty} specialist, analyze the following clinician-patient conversation:

#         {conversation_text}

#         Return ONLY a valid JSON object with this structure — no markdown, no explanations:

#         {
#             "missing_elements": [...],
#             "alerts": [...],
#             "structured_data": {
#                 "Symptoms": [...],
#                 "Medications": [...],
#                 "Allergies": [...],
#                 "Conditions": [...]
#             }
#         }
       
#         """)
#         self.chain = LLMChain(llm=self.llm, prompt=self.template)

#     def run(self, conversation_text: str) -> str:
#         return self.chain.run({
#             "conversation_text": conversation_text,
#             "specialty": self.clinician_specialty
#         })
# agents/dialogue_agent.py

from llm_setup import get_llm
from langchain.prompts import PromptTemplate

class DialogueAgent:
    def __init__(self, clinician_specialty: str = "general"):
        self.clinician_specialty = clinician_specialty
        self.llm = get_llm()  # Uses Groq-hosted model via ChatGroq

        self.template = PromptTemplate(
            input_variables=["conversation_text", "specialty"],
            template="""
You are a {specialty} specialist. Analyze the following clinician-patient conversation (plain text):

{conversation_text}

Your task:
- DO NOT repeat the input verbatim.
- Summarize and rephrase the information in your own words.
- Use clear, structured formatting with proper sections.
- If information is missing, state 'Not provided'.

Respond in this structured format:

**Patient Information:**
- Name: <name if available>
- Age: <age if available>
- Gender: <gender if available>
- Date of Visit: <date if available>

**Conversation Analysis:**

**Missing Elements:**
• <bullet points about information that should have been collected>

**Clinical Alerts:**
• <bullet points about concerning symptoms, red flags, urgent issues>

**Structured Data:**

**Symptoms:**
• <bullet points about reported symptoms>

**Medications:**
• <bullet points about current medications>

**Allergies:**
• <bullet points about known allergies>

**Conditions:**
• <bullet points about medical conditions, diagnoses>

Use professional medical language and ensure each section is clearly separated.
"""
        )
        self.chain = self.template | self.llm

    def run(self, conversation_text: str) -> str:
        result = self.chain.invoke({
            "conversation_text": conversation_text,
            "specialty": self.clinician_specialty
        })
        
        # Handle AIMessage objects (from LangChain)
        if hasattr(result, 'content'):
            return result.content
        # Handle dictionaries
        elif isinstance(result, dict):
            if 'content' in result:
                return result['content']
            elif 'text' in result:
                return result['text']
            elif 'response' in result:
                return result['response']
            else:
                return str(result)
        elif isinstance(result, str):
            return result
        else:
            return str(result)

