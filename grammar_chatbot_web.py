import streamlit as st
import json

# Load lessons from file
@st.cache_data
def load_lessons():
    with open("grammar_lessons.json", "r") as file:
        data = json.load(file)
    return data["lessons"]

lessons = load_lessons()

# Memory state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_lesson" not in st.session_state:
    st.session_state.last_lesson = None

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

# Streamlit UI
st.title("📚 English Grammar Chatbot")

# Display chat messages in order, with latest at the bottom
chat_container = st.container()

with chat_container:
    for speaker, message in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {message}")

# A small spacer to create distance before the input field
st.markdown("---")

# Keep input at the bottom
input_container = st.container()

with input_container:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type your message and press Enter:")
        submitted = st.form_submit_button("Send")

        if submitted and user_input:
            response = get_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))
            st.experimental_rerun()  # Auto-scrolls to bottom by re-running the app


