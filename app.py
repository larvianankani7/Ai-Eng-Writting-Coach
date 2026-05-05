import streamlit as st

from loaders.text_loader import load_text_file
from loaders.pdf_loader import load_pdf
from loaders.web_loader import load_web

from processing.pipeline import process_text
from ai.coach import review_text

# -----------------------------
# 🎨 PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Writing Coach",
    page_icon="✍️",
    layout="wide"
)

# -----------------------------
# 🎨 MODERN UI STYLING
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #0f1117;
    color: white;
}

/* Main container */
.block-container {
    padding: 2rem 3rem;
}

/* Title */
h1 {
    font-size: 2.8rem !important;
    font-weight: 700;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    border: none;
    transition: 0.2s ease-in-out;
}

.stButton button:hover {
    transform: scale(1.03);
}

/* Text area */
textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("✍️ AI Writing Coach")
st.caption("Improve grammar • clarity • tone instantly using AI")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("⚙️ Options")

    input_mode = st.radio(
        "Choose input type",
        ["Text", "File", "Web URL"]
    )

    st.write("---")
    st.info("💡 Tip: Clear sentences give better AI feedback")

# -----------------------------
# INPUT HANDLING
# -----------------------------
text_data = ""

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown("### 📝 Input")

    if input_mode == "Text":
        text_data = st.text_area("Write or paste your text here", height=250)

    elif input_mode == "File":
        file = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])

        if file:
            if file.name.endswith(".txt"):
                text_data = file.read().decode("utf-8")

            elif file.name.endswith(".pdf"):
                with open("temp.pdf", "wb") as f:
                    f.write(file.read())
                text_data = load_pdf("temp.pdf")

            st.success("File loaded successfully!")

    elif input_mode == "Web URL":
        url = st.text_input("Enter website URL")

        if url:
            text_data = load_web(url)
            st.success("Web content loaded!")

# -----------------------------
# ACTION PANEL
# -----------------------------
with col2:
    st.markdown("### 📊 Insights")

    st.markdown("""
    <div class="card">
    ✨ Grammar correction<br>
    ✨ Sentence improvement<br>
    ✨ Tone analysis<br>
    ✨ Writing feedback
    </div>
    """, unsafe_allow_html=True)

    run_btn = st.button("🚀 Analyze Writing")

# -----------------------------
# AI PROCESSING
# -----------------------------
if run_btn:

    if text_data.strip():

        with st.spinner("AI is analyzing your writing..."):

            # Step 1: process text
            chunks = process_text(text_data)

            # Step 2: AI review
            result = review_text(chunks[0])

        st.markdown("### 📌 AI Feedback")

        st.success(result)

    else:
        st.warning("Please enter or upload some text first")