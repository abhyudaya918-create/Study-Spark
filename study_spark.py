import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Planner App",
    page_icon="📚",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "summary_output" not in st.session_state:
    st.session_state.summary_output = ""
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = ""
if "schedule_output" not in st.session_state:
    st.session_state.schedule_output = ""

# --- SIDEBAR UI ---
st.sidebar.title("🔑 Control Panel")

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your API key here for OpenAI processing."
)

uploaded_file = st.sidebar.file_uploader("Upload Text File", type=["txt"])

if uploaded_file is not None:
    st.session_state.document_text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.sidebar.success("File uploaded successfully!")

st.sidebar.divider()
study_days = st.sidebar.slider("Schedule Duration (Days)", 1, 14, 5)
hours_per_day = st.sidebar.slider("Hours per Day", 1, 6, 2)

process_btn = st.sidebar.button("🚀 Process & Generate Plan", type="primary")

# --- GENERATION LOGIC ---
if process_btn:
    text = st.session_state.document_text.strip()
    
    if not text:
        st.sidebar.error("Please paste text or upload a file first.")
    else:
        # Fallback text-based generation using native Streamlit state logic
        lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 10]
        
        # 1. Summary Generation
        if len(lines) >= 3:
            st.session_state.summary_output = "\n".join([f"- {line}" for line in lines[:4]])
        else:
            st.session_state.summary_output = f"- {text[:300]}..."
            
        # 2. Quiz Generation
        quiz_text = ""
        for i in range(min(3, max(1, len(lines)))):
            line = lines[i] if i < len(lines) else text
            words = line.split()
            if len(words) > 4:
                question = " ".join(words[: len(words)//2]) + " _______ " + " ".join(words[len(words)//2 + 1 :])
                answer = words[len(words)//2]
                quiz_text += f"**Q{i+1}: Fill in the blank**\n{question}\n\n*Answer:* {answer}\n\n---\n"
            else:
                quiz_text += f"**Q{i+1}: Concept Check**\nWhat is the main idea of: '{line[:50]}'?\n\n---\n"
        st.session_state.quiz_output = quiz_text
        
        # 3. Schedule Generation
        schedule_text = ""
        for day in range(1, study_days + 1):
            schedule_text += f"**Day {day}:** Study for **{hours_per_day} hours**. Focus on Topic Section {day}.\n\n"
        st.session_state.schedule_output = schedule_text
        
        st.sidebar.success("Generated successfully!")

# --- MAIN INTERFACE ---
st.title("🎓 Student Planner & Learning Companion")

if openai_api_key:
    st.info(f"OpenAI API Key entered: `{openai_api_key[:4]}...{openai_api_key[-4:]}`")

if not st.session_state.document_text:
    st.session_state.document_text = st.text_area("Paste your study text here directly:", height=200)

tab1, tab2, tab3 = st.tabs(["📝 Executive Summary", "🧠 Quiz", "📅 Study Schedule"])

with tab1:
    st.header("Executive Summary")
    if st.session_state.summary_output:
        st.markdown(st.session_state.summary_output)
    else:
        st.caption("Click 'Process & Generate Plan' to view the summary.")

with tab2:
    st.header("Self-Assessment Quiz")
    if st.session_state.quiz_output:
        st.markdown(st.session_state.quiz_output)
    else:
        st.caption("Click 'Process & Generate Plan' to view the quiz.")

with tab3:
    st.header("Automated Study Plan")
    if st.session_state.schedule_output:
        st.markdown(st.session_state.schedule_output)
    else:
        st.caption("Click 'Process & Generate Plan' to view the study schedule.")