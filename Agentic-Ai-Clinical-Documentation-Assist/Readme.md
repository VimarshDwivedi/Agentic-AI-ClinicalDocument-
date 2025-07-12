
# Agentic System for Clinical Assistant

This project implements a clinical assistant system that uses multiple agents to process patient data, analyze doctor-patient conversations, generate medical documentation, and generate billing codes. The system is built using FastAPI and LangChain, with agents handling various tasks like pre-visit summaries, conversation analysis, SOAP note generation, and code generation.

## **Project Structure**

backend/
├── main.py # FastAPI app setup and routes
├── agents/ # Contains all agent logic
│ ├── preparation_agent.py # Pre-visit summary agent
│ ├── dialogue_agent.py # Conversation analysis agent
│ ├── note_generator_agent.py # SOAP note generation agent
│ └── coder_agent.py # Billing code generation agent
├── sample_data/ # Sample data files (JSON, text)
│ ├── sample_patient.json # Sample patient data (FHIR-like)
│ └── sample_conversation.txt # Sample conversation between doctor and patient
├── requirements.txt # Python dependencies
└── test_flow.py # Flow to test the system end-to-end

csharp
Copy
Edit

## **Installation**

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## **Setup**

1. Ensure that all required files (such as `sample_patient.json` and `sample_conversation.txt`) are in place under the `sample_data/` directory.
2. Update any necessary configurations in the agent files (e.g., LLM setup, conversation logic).

## **API Endpoints**

### **1. Generate Pre-Visit Summary**
- **Endpoint:** `POST /generate-summary`
- **Purpose:** Generates a pre-visit summary based on a patient's EHR data.
  
#### **Request Body:**
```json
{
  "patient_info": {
    "resourceType": "Patient",
    "id": "example",
    "active": true,
    "name": [{"text": "John Doe"}],
    "gender": "male",
    "birthDate": "1980-05-15",
    "conditions": [
      {
        "code": {"text": "Type 2 Diabetes"},
        "onsetDate": "2020-03-01",
        "lastUpdated": "2023-01-15"
      }
    ],
    "observations": [
      {
        "code": {"text": "HbA1c"},
        "value": 7.2,
        "date": "2023-01-10",
        "trend": "up from 6.8 6 months ago"
      }
    ],
    "medications": [
      {
        "medication": {"text": "Metformin 500mg"},
        "status": "active",
        "adherence": "partial"
      }
    ]
  }
}
Response:
json
Copy
Edit
{
  "summary": "Pre-visit summary generated based on patient EHR: \n- Key metrics trend: HbA1c up from 6.8 to 7.2\n- Issues needing follow-up: Type 2 Diabetes\n- Medication adherence: Partial adherence to Metformin\n- Screenings due: None."
}
2. Analyze Conversation
Endpoint: POST /analyze-conversation

Purpose: Analyzes a conversation between a doctor and a patient to detect possible health issues or alerts.

Request Body:
json
Copy
Edit
{
  "conversation_text": "Doctor: How have you been feeling since your last visit? Patient: Not great, my blood sugar has been high. Doctor: Are you taking your Metformin regularly? Patient: I try to, but sometimes I forget."
}
Response:
json
Copy
Edit
{
  "analysis": {
    "alerts": [
      "Blood sugar levels are high. Recommend follow-up.",
      "Partial adherence to Metformin. Possible issue with medication adherence."
    ],
    "structured_data": {
      "condition": "Type 2 Diabetes",
      "medication": "Metformin 500mg",
      "adherence": "partial"
    }
  }
}
3. Generate SOAP Note
Endpoint: POST /generate-note

Purpose: Generates a SOAP (Subjective, Objective, Assessment, Plan) note based on patient information.

Request Body:
json
Copy
Edit
{
  "patient_info": {
    "resourceType": "Patient",
    "id": "example",
    "active": true,
    "name": [{"text": "John Doe"}],
    "gender": "male",
    "birthDate": "1980-05-15",
    "conditions": [
      {
        "code": {"text": "Type 2 Diabetes"},
        "onsetDate": "2020-03-01",
        "lastUpdated": "2023-01-15"
      }
    ],
    "observations": [
      {
        "code": {"text": "HbA1c"},
        "value": 7.2,
        "date": "2023-01-10",
        "trend": "up from 6.8 6 months ago"
      }
    ],
    "medications": [
      {
        "medication": {"text": "Metformin 500mg"},
        "status": "active",
        "adherence": "partial"
      }
    ]
  }
}
Response:
json
Copy
Edit
{
  "soap_note": {
    "S": "Patient reports feeling unwell due to high blood sugar. Complains of partial adherence to medication.",
    "O": "HbA1c level 7.2, trend: up from 6.8 six months ago.",
    "A": "Type 2 Diabetes, partial adherence to Metformin.",
    "P": "Continue monitoring HbA1c levels, recommend better medication adherence."
  }
}
4. Generate Billing Codes
Endpoint: POST /generate-codes

Purpose: Generates relevant billing codes based on patient information.

Request Body:
json
Copy
Edit
{
  "patient_info": {
    "resourceType": "Patient",
    "id": "example",
    "active": true,
    "name": [{"text": "John Doe"}],
    "gender": "male",
    "birthDate": "1980-05-15",
    "conditions": [
      {
        "code": {"text": "Type 2 Diabetes"},
        "onsetDate": "2020-03-01",
        "lastUpdated": "2023-01-15"
      }
    ],
    "observations": [
      {
        "code": {"text": "HbA1c"},
        "value": 7.2,
        "date": "2023-01-10",
        "trend": "up from 6.8 6 months ago"
      }
    ],
    "medications": [
      {
        "medication": {"text": "Metformin 500mg"},
        "status": "active",
        "adherence": "partial"
      }
    ]
  }
}
Response:
json
Copy
Edit
{
  "codes": [
    {
      "code": "E11.9",
      "description": "Type 2 Diabetes Mellitus, Uncomplicated"
    },
    {
      "code": "Z79.4",
      "description": "Long-term (current) use of oral hypoglycemic drugs"
    }
  ]
}
Testing
To test the entire workflow, use the test_flow.py script. This script simulates an end-to-end interaction with the system, including loading sample data, generating summaries, analyzing conversations, and generating SOAP notes and billing codes.

Run the test:
bash
Copy
Edit
python test_flow.py
