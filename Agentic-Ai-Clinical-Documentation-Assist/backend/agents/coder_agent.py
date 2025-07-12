from llm_setup import get_llm
from langchain.prompts import PromptTemplate

class CoderAgent:
    def __init__(self):
        self.llm = get_llm()  # Uses Groq-hosted model via ChatGroq
        self.template = PromptTemplate(
            input_variables=["structured_data"],
            template="""
You are a medical billing expert. Given the following structured clinical data (plain text):

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

**Billing Codes:**

**ICD-11 Codes:**
• <code>: <description> - <rationale>
• <code>: <description> - <rationale>

**CPT Codes:**
• <code>: <description> - <rationale>
• <code>: <description> - <rationale>

**E/M Level:**
• Level: <level> - <justification>

Use professional medical language and ensure each section is clearly separated.
"""
        )
        self.chain = self.template | self.llm

    def run(self, structured_data: str) -> str:
        try:
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
        except Exception as e:
            return f"Error generating codes: {str(e)}"
