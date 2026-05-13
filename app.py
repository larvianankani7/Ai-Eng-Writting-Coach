import streamlit as st

from loaders.text_loader import load_text_file
from loaders.pdf_loader import load_pdf
from loaders.web_loader import load_web
from processing.pipeline import process_text
from ai.coach import review_text

# -----------------------------
# ⚙️ PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Writing Coach",
    page_icon="✍️",
    layout="wide"
)

# -----------------------------
# 🎨 MODERN UI STYLE
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #0f1117;
    color: white;
}

.block-container {
    padding: 2rem 3rem;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 700;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 10px;
}

.stButton button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    border: none;
}

.stButton button:hover {
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("✍️ AI English Writing Coach")
st.caption("Improve grammar, clarity and tone using AI")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.header("⚙️ Input Options")

    input_mode = st.radio(
        "Choose input type",
        ["Text", "File", "Web URL"]
    )

    st.write("---")

    st.info("💡 Tip: Clear input gives better AI feedback")

# -----------------------------
# INPUT AREA
# -----------------------------
text_data = ""

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown("### 📝 Input")

    if input_mode == "Text":

        text_data = st.text_area(
            "Write your text here",
            height=250
        )

    elif input_mode == "File":

        file = st.file_uploader(
            "Upload TXT or PDF",
            type=["txt", "pdf"]
        )

        if file:

            if file.name.endswith(".txt"):

                text_data = file.read().decode("utf-8")

            elif file.name.endswith(".pdf"):

                with open("temp.pdf", "wb") as f:
                    f.write(file.read())

                text_data = load_pdf("temp.pdf")

            st.success("File loaded!")

    elif input_mode == "Web URL":

        url = st.text_input("Enter URL")

        if url:

            text_data = load_web(url)

            st.success("Web content loaded!")

# -----------------------------
# INSIGHTS PANEL
# -----------------------------
with col2:

    st.markdown("### 📊 Insights Panel")

    st.markdown("""
    <div class="card">
    ✨ Grammar check<br>
    ✨ Sentence improvement<br>
    ✨ Tone analysis<br>
    ✨ AI suggestions<br>
    ✨ Vocabulary enhancement
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# ACTION BUTTON
# -----------------------------
run_btn = st.button("🚀 Analyze Writing")

# -----------------------------
# AI PROCESSING + OUTPUT
# -----------------------------
if run_btn:

    if not text_data.strip():

        st.warning("Please enter some text first")

    else:

        with st.spinner("AI is analyzing your writing..."):

            chunks = process_text(text_data)

            result = review_text(chunks[0])

        # -----------------------------
        # RESULTS
        # -----------------------------
        st.markdown("## ✨ Corrected Text")

        st.success(result["corrected_text"])

        # COPY VIEW
        st.code(result["corrected_text"])

        # -----------------------------
        # SCORE + TONE
        # -----------------------------
        colA, colB = st.columns(2)

        with colA:

            st.markdown("## 📊 Score")

            st.progress(result["score"] / 100)

            st.write(f"{result['score']}/100")

        with colB:

            st.markdown("## 🎯 Tone")

            st.info(result["tone"])

        # -----------------------------
        # GRAMMAR ERRORS
        # -----------------------------
        st.markdown("## 🚨 Grammar Mistakes")

        if result["grammar_errors"]:

            for g in result["grammar_errors"]:

                st.write("•", g)

        else:

            st.success("No major grammar issues found 🎉")

        # -----------------------------
        # SUGGESTIONS
        # -----------------------------
        st.markdown("## 💡 Suggestions")

        if result["suggestions"]:

            for s in result["suggestions"]:

                st.write("•", s)

        else:

            st.info("No suggestions available.")

        # -----------------------------
        # VOCABULARY ENHANCEMENT
        # -----------------------------
        st.markdown("## 📚 Vocabulary Enhancement")

        if result.get("vocabulary_enhancements"):

            for vocab in result["vocabulary_enhancements"]:

                original = vocab.get("original", "")
                replacement = vocab.get("replacement", "")

                st.markdown(f"""
                <div class="card">
                🔹 <b>{original}</b>
                →
                <span style='color:#8b5cf6'>
                <b>{replacement}</b>
                </span>
                </div>
                """, unsafe_allow_html=True)

        else:

            st.info("No vocabulary improvements suggested.")

        # -----------------------------
        # SUMMARY
        # -----------------------------
        st.markdown("## 🧠 Summary")

        st.write(result["summary"])

        # -----------------------------
        # BUTTONS
        # -----------------------------
        b1, b2 = st.columns(2)

        with b1:

            if st.button("📋 Copy Text"):

                st.code(result["corrected_text"])

        with b2:

            if st.button("🔁 Re-analyze"):

                st.rerun()
