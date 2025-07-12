from llm_setup import get_llm
from langchain.prompts import PromptTemplate

class NoteGeneratorAgent:
    def __init__(self):
        self.llm = get_llm()  # Uses Groq-hosted model via ChatGroq
        self.template = PromptTemplate.from_template("""
        Generate a SOAP note from the following structured medical data (plain text):

        {structured_data}

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

        **SOAP Note:**

        **Subjective:**
        • <bullet points about patient's reported symptoms, history, concerns>

        **Objective:**
        • <bullet points about vital signs, physical exam findings, lab results>

        **Assessment:**
        • <bullet points about diagnoses, differential diagnoses, clinical impressions>

        **Plan:**
        • <bullet points about treatment plan, medications, follow-up, referrals>

        Use professional medical language and ensure each section is clearly separated.
        """)
        self.chain = self.template | self.llm

    def run(self, structured_data: str) -> str:
        result = self.chain.invoke({"structured_data": structured_data})
        
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
