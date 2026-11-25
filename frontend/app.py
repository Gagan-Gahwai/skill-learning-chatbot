
import streamlit as st
import sys
from pathlib import Path

# Make project root accessible for imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from crawler.rag_pipeline import ask_question


# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Website Knowledge AI",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------
# 2. CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}

.chat-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #1e3a8a;
}

.chat-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# 3. SIDEBAR
# --------------------------------

with st.sidebar:

    st.title("🤖 Website AI")

    st.caption("Your intelligent website assistant")

    st.divider()

    st.subheader("About")

    st.write(
        "Ask questions about Skill Learning Academy. "
        "Our AI assistant searches website content "
        "and generates answers using RAG."
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Ollama + ChromaDB")


# --------------------------------
# 4. MAIN HEADER
# --------------------------------

st.markdown(
    '<div class="chat-title">Website Knowledge AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-subtitle">'
    'Ask anything about Skill Learning Academy'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# 5. CHAT HISTORY
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"- [{source['title']}]({source['url']})"
                    )


# --------------------------------
# 6. CHAT INPUT
# --------------------------------

question = st.chat_input("Ask your question here...")


if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)


    # Generate AI answer
    with st.chat_message("assistant"):

        with st.spinner("Searching website knowledge..."):

            try:

                answer = ask_question(question)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    "Something went wrong while generating the answer."
                )

                st.exception(error)
