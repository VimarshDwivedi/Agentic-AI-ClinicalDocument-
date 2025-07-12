from llm_setup import get_llm
from langchain.prompts import PromptTemplate

class PreparationAgent:
    def __init__(self):
        self.llm = get_llm()  # Uses Groq-hosted model via ChatGroq
        self.template = PromptTemplate.from_template("""
        Analyze the following patient EHR summary (plain text):

        {input_text}

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

        **Pre-Visit Summary:**

        **Key Metrics Trend:**
        • <bullet points about vital signs, lab values, trends>

        **Issues Needing Follow-up:**
        • <bullet points about concerns, complications, red flags>

        **Medication Adherence:**
        • <bullet points about current medications and adherence>

        **Screenings Due:**
        • <bullet points about recommended screenings, tests, follow-ups>

        Use professional medical language and ensure each section is clearly separated.
        """)
        self.chain = self.template | self.llm

    def run(self, patient_info: str) -> str:
        result = self.chain.invoke({"input_text": patient_info})
        
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
