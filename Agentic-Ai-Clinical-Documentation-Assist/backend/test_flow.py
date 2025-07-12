# backend/test_flow.py
from agents.preparation_agent import PreparationAgent
from agents.dialogue_agent import DialogueAgent
from agents.note_generator_agent import NoteGeneratorAgent
from agents.coder_agent import CoderAgent

def test_flow():
    # Load sample patient data
    with open("sample_data/sample_patient.json") as f:
        import json
        patient_data = json.load(f)

    # Step 1: Generate pre-visit summary
    prep_agent = PreparationAgent()
    summary = prep_agent.run(json.dumps(patient_data, indent=2))
    print("📝 Pre-Visit Summary:\n", summary)

    # Step 2: Analyze conversation
    with open("sample_data/sample_conversation.txt") as f:
        conversation = f.read()

    dialogue_agent = DialogueAgent("cardiology")
    analysis_output = dialogue_agent.run(conversation)
    print("\n📢 Dialogue Analysis:\n", analysis_output)

    # Step 3: Generate SOAP note (using the conversation analysis as input)
    note_agent = NoteGeneratorAgent()
    soap_note = note_agent.run(analysis_output)
    print("\n📄 SOAP Note:\n", soap_note)

    # Step 4: Generate Billing Codes (using the conversation analysis as input)
    coder_agent = CoderAgent()
    codes = coder_agent.run(analysis_output)
    print("\n💰 Billing Codes:\n", codes)

if __name__ == "__main__":
    test_flow()
