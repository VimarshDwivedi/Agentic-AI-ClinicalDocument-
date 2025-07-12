# aap.py
import streamlit as st
import os
import sys

# Configure the page
st.set_page_config(
    page_title="Clinical Documentation Assistant",
    page_icon="🏥",
    layout="wide"
)

# Add the current directory to Python path to ensure module visibility
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Core imports
from dotenv import load_dotenv
from agents.preparation_agent import PreparationAgent
from agents.dialogue_agent import DialogueAgent
from agents.note_generator_agent import NoteGeneratorAgent
from agents.coder_agent import CoderAgent

def initialize_session_state():
    """Initialize session state variables"""
    if 'prep_agent' not in st.session_state:
        st.session_state.prep_agent = PreparationAgent()
    if 'dialogue_agent' not in st.session_state:
        st.session_state.dialogue_agent = DialogueAgent()
    if 'note_agent' not in st.session_state:
        st.session_state.note_agent = NoteGeneratorAgent()
    if 'coder_agent' not in st.session_state:
        st.session_state.coder_agent = CoderAgent()

def setup_sidebar():
    """Setup the sidebar with information"""
    with st.sidebar:
        st.header("🏥 Clinical Documentation Assistant")
        st.markdown("---")
        st.markdown("**Features:**")
        st.markdown("• Pre-Visit Summary Generation")
        st.markdown("• Conversation Analysis")
        st.markdown("• SOAP Note Generation")
        st.markdown("• Billing Code Generation")
        st.markdown("---")
        st.markdown("**Instructions:**")
        st.markdown("1. Select the appropriate tab")
        st.markdown("2. Enter patient information as plain text")
        st.markdown("3. Click generate to get structured output")
        st.markdown("---")
        st.markdown("**Powered by:**")
        st.markdown("• Groq LLM API")
        st.markdown("• LangChain")
        st.markdown("• Streamlit")

def setup_preparation_agent_tab():
    """Setup the Pre-Visit Summary tab"""
    st.header("📋 Pre-Visit Summary Generator")
    st.markdown("Generate structured pre-visit summaries from patient EHR information.")
    
    patient_info = st.text_area(
        "Enter patient EHR information (plain text):",
        height=200,
        placeholder="Enter patient details, medical history, current medications, lab results, etc..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Generate Summary", type="primary"):
            if patient_info:
                with st.spinner("Generating pre-visit summary..."):
                    try:
                        summary = st.session_state.prep_agent.run(patient_info)
                        st.success("Summary generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
                        return
            else:
                st.warning("Please enter patient information first.")
                return
    
    # Display results
    if 'summary' in locals():
        st.subheader("📄 Pre-Visit Summary")
        st.markdown(summary)

def setup_dialogue_agent_tab():
    """Setup the Conversation Analysis tab"""
    st.header("💬 Conversation Analysis")
    st.markdown("Analyze clinician-patient conversations for missing elements and clinical alerts.")
    
    conversation_text = st.text_area(
        "Enter clinician-patient conversation (plain text):",
        height=200,
        placeholder="Enter the conversation between doctor and patient..."
    )
    
    specialty = st.selectbox(
        "Select specialty:",
        ["general", "cardiology", "neurology", "pediatrics", "orthopedics", "dermatology", "psychiatry"]
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔍 Analyze Conversation", type="primary"):
            if conversation_text:
                with st.spinner("Analyzing conversation..."):
                    try:
                        st.session_state.dialogue_agent.clinician_specialty = specialty
                        analysis = st.session_state.dialogue_agent.run(conversation_text)
                        st.success("Analysis completed successfully!")
                    except Exception as e:
                        st.error(f"Error analyzing conversation: {str(e)}")
                        return
            else:
                st.warning("Please enter conversation text first.")
                return
    
    # Display results
    if 'analysis' in locals():
        st.subheader("📊 Conversation Analysis Result")
        st.markdown(analysis)

def setup_note_generator_tab():
    """Setup the SOAP Note Generator tab"""
    st.header("📝 SOAP Note Generator")
    st.markdown("Generate structured SOAP notes from medical data.")
    
    structured_data = st.text_area(
        "Enter structured medical data (plain text):",
        height=200,
        placeholder="Enter patient symptoms, exam findings, lab results, etc..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📋 Generate SOAP Note", type="primary"):
            if structured_data:
                with st.spinner("Generating SOAP note..."):
                    try:
                        soap_note = st.session_state.note_agent.run(structured_data)
                        st.success("SOAP note generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating SOAP note: {str(e)}")
                        return
            else:
                st.warning("Please enter structured data first.")
                return
    
    # Display results
    if 'soap_note' in locals():
        st.subheader("📄 SOAP Note")
        st.markdown(soap_note)

def setup_coder_agent_tab():
    """Setup the Billing Code Generator tab"""
    st.header("💰 Billing Code Generator")
    st.markdown("Generate appropriate billing codes and documentation from clinical data.")
    
    structured_data = st.text_area(
        "Enter structured medical data for coding (plain text):",
        height=200,
        placeholder="Enter diagnosis, procedures, symptoms, etc..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💳 Generate Codes", type="primary"):
            if structured_data:
                with st.spinner("Generating billing codes..."):
                    try:
                        codes = st.session_state.coder_agent.run(structured_data)
                        st.success("Billing codes generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating billing codes: {str(e)}")
                        return
            else:
                st.warning("Please enter structured data first.")
                return
    
    # Display results
    if 'codes' in locals():
        st.subheader("💳 Billing Codes")
        st.markdown(codes)

def main():
    # Load environment variables
    load_dotenv()

    # Initialize session state
    initialize_session_state()
    
    st.title("🏥 Clinical Documentation Assistant")
    
    # Setup sidebar
    setup_sidebar()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Pre-Visit Summary", 
        "💬 Conversation Analysis", 
        "📝 SOAP Note Generator", 
        "💰 Billing Codes"
    ])
    
    with tab1:
        setup_preparation_agent_tab()
    
    with tab2:
        setup_dialogue_agent_tab()
    
    with tab3:
        setup_note_generator_tab()
    
    with tab4:
        setup_coder_agent_tab()

    # Custom CSS styling
    st.markdown("""
    <style>
        /* Background color */
        .stApp {
            background-color: #e6f2f2; /* Light teal */
        }

        /* Title styling */
        h1 {
            color: #00796b; /* Teal */
            text-align: center;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            background-color: #b2dfdb;  /* Lighter teal */
            color: #004d40;
            font-weight: bold;
            border-radius: 10px 10px 0 0;
            padding: 10px;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #80cbc4;
            color: #00332d;
        }

        .stTabs [aria-selected="true"] {
            background-color: #4dd0e1 !important;
            color: white !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #b2dfdb;
        }

        /* Buttons */
        .stButton > button {
            background-color: #00796b;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #004d40;
        }

        /* Text areas */
        .stTextArea > div > div > textarea {
            border-radius: 10px;
            border: 2px solid #b2dfdb;
        }

        /* Success messages */
        .stSuccess {
            background-color: #c8e6c9;
            border-radius: 10px;
            padding: 10px;
        }

        /* Warning messages */
        .stWarning {
            background-color: #fff3e0;
            border-radius: 10px;
            padding: 10px;
        }

        /* Error messages */
        .stError {
            background-color: #ffcdd2;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()