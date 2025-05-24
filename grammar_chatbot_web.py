import streamlit as st
import json

# Load lessons from file
@st.cache_data
def load_lessons():
    with open("grammar_lessons.json", "r") as file:
        data = json.load(file)
    return data["lessons"]

lessons = load_lessons()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_lesson" not in st.session_state:
    st.session_state.last_lesson = None

if "user_input_text" not in st.session_state:
    st.session_state.user_input_text = ""

# Bot response logic
def get_response(user_input):
    user_input = user_input.lower().strip()

    if user_input in ["exit", "quit", "bye"]:
        return "Goodbye! Keep practicing! 💡"
    elif user_input == "menu":
        response = "📘 English Grammar Lessons\n"
        for key, value in lessons.items():
            response += f"{key}. {value['title']}\n"
        return response
    elif user_input in lessons:
        lesson = lessons[user_input]
        st.session_state.last_lesson = user_input
        examples = "\n".join([f"✔ {ex}" for ex in lesson["examples"]])
        return f"📖 Lesson {user_input}: {lesson['title']}\n{lesson['content']}\n\nExamples:\n{examples}"
    elif "example" in user_input:
        last_id = st.session_state.last_lesson
        if last_id and last_id in lessons:
            examples = "\n".join([f"✔ {ex}" for ex in lessons[last_id]["examples"]])
            return f"Here are more examples:\n{examples}"
        else:
            return "❌ Please select a lesson first using 'menu'."
    else:
        return "🤖 I didn't understand that. Type 'menu' to see available lessons."

# App title
st.title("📚 English Grammar Chatbot")

# Display chat history (top)
with st.container():
    for speaker, message in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {message}")

# Input field (fixed at bottom)
user_input = st.text_input(
    "💬 Type your message and press Enter:",
    key="user_input_text"
)

if user_input:
    response = get_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))
    st.session_state.user_input_text = ""  # Clear input safely
    st.experimental_rerun()  # Rerun app to simulate auto-scroll
