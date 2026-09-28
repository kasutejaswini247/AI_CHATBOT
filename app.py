import streamlit as st
import ollama

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Friendly AI Bot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN APP
   ===================================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #050505,
        #101827,
        #050505
    );
    color: white;
}


/* Main container */

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   HEADINGS
   ===================================================== */

h1 {
    text-align: center;
    color: #00e5ff !important;
    font-size: 45px !important;
    font-weight: 800 !important;
    text-shadow: 0 0 15px #00e5ff;
    letter-spacing: 2px;
}

h2 {
    text-align: center;
    color: #00ffcc !important;
}

h3 {
    text-align: center;
    color: #b8c7d9 !important;
}


/* Normal text */

p {
    color: #d7dee8 !important;
}


/* =====================================================
   CHAT INPUT
   ===================================================== */

.stChatInput textarea {
    background-color: #111827 !important;
    color: white !important;
    border: 1px solid #00e5ff !important;
    border-radius: 12px !important;
}

.stChatInput textarea::placeholder {
    color: #8b9aaa !important;
}


/* =====================================================
   CHAT MESSAGES
   ===================================================== */

[data-testid="stChatMessage"] {
    background-color: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #080d16;
}


/* Sidebar title */

section[data-testid="stSidebar"] h1 {
    font-size: 28px !important;
    text-shadow: none;
}


/* =====================================================
   SIDEBAR BUTTONS
   ===================================================== */

/* Dark button with clear text */

section[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    background-color: #111827 !important;

    color: #ffffff !important;

    border: 1px solid #334155 !important;

    border-radius: 10px !important;

    font-weight: 600 !important;

    padding: 9px !important;

    transition: 0.3s;
}


/* Sidebar button hover */

section[data-testid="stSidebar"] .stButton > button:hover {

    background-color: #172554 !important;

    color: #00e5ff !important;

    border: 1px solid #00e5ff !important;

    box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);

}


/* =====================================================
   MAIN BUTTON - CLEAR CHAT
   ===================================================== */

.stButton > button {

    background-color: #1f2937 !important;

    color: #ffffff !important;

    border: 1px solid #475569 !important;

    border-radius: 10px !important;

    font-weight: bold !important;

    padding: 10px;

    transition: 0.3s;
}


/* Clear Chat hover */

.stButton > button:hover {

    background-color: #7f1d1d !important;

    color: #ffffff !important;

    border: 1px solid #ef4444 !important;

    box-shadow: 0 0 12px rgba(239, 68, 68, 0.35);

}


/* =====================================================
   SELECT BOX
   ===================================================== */

[data-baseweb="select"] {
    background-color: #111827 !important;
    border-radius: 10px;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color: #00e5ff !important;
    opacity: 0.3;
}


/* =====================================================
   CAPTION
   ===================================================== */

.stCaption {
    color: #8b9aaa !important;
    text-align: center;
}


/* =====================================================
   SCROLLBAR
   ===================================================== */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #050505;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00e5ff;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.chats[
        st.session_state.current_chat
    ] = []


# =========================================================
# SIDEBAR - CHAT HISTORY
# =========================================================

with st.sidebar:

    st.title("💬 Chat History")

    # New Chat
    if st.button("➕ New Chat"):

        chat_number = len(
            st.session_state.chats
        ) + 1

        new_chat = f"Chat {chat_number}"

        st.session_state.chats[new_chat] = []

        st.session_state.current_chat = new_chat

        st.rerun()

    st.divider()

    # Previous chats
    for chat_name in st.session_state.chats:

        if st.button(
            chat_name,
            key=f"chat_{chat_name}"
        ):

            st.session_state.current_chat = chat_name

            st.rerun()

    st.divider()

    st.caption(
        f"Current chat: {st.session_state.current_chat}"
    )


# =========================================================
# HEADER
# =========================================================

st.title("🤖 Friendly AI Bot")

st.header("Your Intelligent AI Assistant")

st.subheader(
    "Ask questions and get intelligent answers instantly."
)

st.caption(
    "Powered by Streamlit + Ollama + Llama 3.2"
)


# =========================================================
# MODEL SELECTION
# =========================================================

st.divider()

model = st.selectbox(
    "Select AI Model",
    [
        "llama3.2",
        "llama3.1"
    ]
)


# =========================================================
# CURRENT CHAT
# =========================================================

messages = st.session_state.chats[
    st.session_state.current_chat
]


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "💬 Type your question here..."
)


# =========================================================
# AI RESPONSE
# =========================================================

if prompt:

    # User message

    with st.chat_message("user"):

        st.markdown(prompt)

    messages.append({
        "role": "user",
        "content": prompt
    })


    # AI response

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 AI is thinking..."
        ):

            try:

                response = ollama.chat(
                    model=model,
                    messages=messages
                )

                answer = response[
                    "message"
                ]["content"]

                st.markdown(answer)

                messages.append({
                    "role": "assistant",
                    "content": answer
                })


            except Exception as e:

                st.error(
                    "Unable to connect to Ollama."
                )

                st.code(str(e))


# =========================================================
# CLEAR CURRENT CHAT
# =========================================================

st.divider()

if st.button(
    "🗑️ Clear Current Chat",
    key="clear_current_chat"
):

    st.session_state.chats[
        st.session_state.current_chat
    ] = []

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Chatbot • Chat History • Local AI • Powered by Ollama"
)