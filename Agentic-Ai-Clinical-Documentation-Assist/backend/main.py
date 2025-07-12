# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from agents.preparation_agent import PreparationAgent
from agents.dialogue_agent import DialogueAgent
from agents.note_generator_agent import NoteGeneratorAgent
from agents.coder_agent import CoderAgent

app = FastAPI()

prep_agent = PreparationAgent()
dialogue_agent = DialogueAgent()
note_agent = NoteGeneratorAgent()
coder_agent = CoderAgent()

class EHRRequest(BaseModel):
    patient_info: dict

class ConversationRequest(BaseModel):
    conversation_text: str

@app.post("/generate-summary")
def generate_summary(request: EHRRequest):
    return {"summary": prep_agent.run(str(request.patient_info))}

@app.post("/analyze-conversation")
def analyze_conversation(request: ConversationRequest):
    result = dialogue_agent.run(request.conversation_text)
    return {"analysis": result}

@app.post("/generate-note")
def generate_note(request: EHRRequest):
    return {"soap_note": note_agent.run(request.patient_info)}

@app.post("/generate-codes")
def generate_codes(request: EHRRequest):
    return {"codes": coder_agent.run(request.patient_info)}

@app.get("/")
def root():
    return {"message": "Agentic AI Clinical Documentation API is running"}

