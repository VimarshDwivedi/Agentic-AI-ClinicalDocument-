# test_dialogue_agent.py
from agents.dialogue_agent import DialogueAgent

def test_dialogue_agent():
    with open("sample_data/sample_conversation.txt") as f:
        conversation = f.read()

    agent = DialogueAgent("cardiology")
    output = agent.run(conversation)
    print("🔍 Analysis Output:\n", output)

if __name__ == "__main__":
    test_dialogue_agent()
