import requests
import streamlit as st
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

# CSS for improved button styling
st.markdown("""
<style>
.stButton>button {
    background-color: #4A90E2;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #357ABD;
}
.stButton>button:active {
    background-color: #285E8E;
}
footer {text-align: center; padding: 10px; font-size: small; color: grey;}
.section-title {
    font-size: 18px;
    font-weight: bold;
    color: #4A90E2;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Function to handle requests to the Wordware API with retry logic
def do_wordware(prompt_url, inputs, retries=3, delay=5):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    for attempt in range(retries):
        response = requests.post(
            prompt_url,
            json={"inputs": inputs},
            headers=headers,
            stream=True
        )
        if response.status_code == 200:
            text_output = ""
            for line in response.iter_lines():
                if line:
                    content = json.loads(line.decode("utf-8"))
                    value = content["value"]
                    if value["type"] == "chunk":
                        text_output += value["value"]
            return text_output
        elif response.status_code == 504:
            print(f"Attempt {attempt + 1}: Gateway timeout. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            break
    return f"Error: Status code {response.status_code}, Details: {response.text or 'Timeout/Server issue'}"

# Function to display topics with context-sensitive "Learn More" options
def display_topics(content, module_name="Module", parent_key="", parent_topic=""):
    # Identify topics by detecting "Topic:" in the content
    topics = [line for line in content.split("\n") if "Topic:" in line]

    # Only create an expander for the main module
    if topics:
        st.markdown(f"<div class='section-title'>{module_name}</div>", unsafe_allow_html=True)
        with st.expander(f"📘 Explore Topics in {module_name}", expanded=False):
            for i, topic in enumerate(topics):
                button_key = f"{parent_key}_learn_more_topic_{i}"
                
                # Display each topic title within the module
                st.markdown(f"**{topic}**")

                # "Learn More" button for each topic within the main module expander
                if not st.session_state.get(f"show_detailed_topic_{button_key}"):
                    if st.button(f"Learn More About {topic.split('Topic: ')[-1].strip()}", key=button_key):
                        st.session_state[f"selected_topic_{button_key}"] = topic.split('Topic: ')[-1].strip()
                        st.session_state[f"show_detailed_topic_{button_key}"] = True
                        # Pass full context including both module and topic to maintain relevance
                        st.session_state[f"context_{button_key}"] = f"{module_name} - {parent_topic} - {topic.split('Topic: ')[-1].strip()}"

                        # Reset other topics in the same module to hide their detailed content
                        for j in range(len(topics)):
                            if j != i:
                                st.session_state[f"show_detailed_topic_{parent_key}_learn_more_topic_{j}"] = False

                # Show detailed content when "Learn More" is clicked
                if st.session_state.get(f"show_detailed_topic_{button_key}"):
                    with st.spinner(f"Fetching more details about {topic.split('Topic: ')[-1].strip()}..."):
                        detailed_inputs = {"SubMod": st.session_state.get(f"context_{button_key}")}  # Use full context
                        detailed_prompt_url = "https://app.wordware.ai/api/released-app/18e4b7f4-57f4-4b41-9797-90eebff79ebf/run"
                        detailed_result = do_wordware(detailed_prompt_url, detailed_inputs)

                        # Display the detailed content as a section within the module without an additional expander
                        if detailed_result:
                            st.markdown("---")  # Divider to separate detailed content
                            st.subheader(f"Details on {topic.split('Topic: ')[-1].strip()}")
                            st.write(detailed_result)





# Function to get modules based on the subject
def get_modules(subject):
    if subject == "Biology":
        return [
            "All Modules",
            "Module 1 - Cells as the Basis of Life",
            "Module 2 - Organisation of Living Things",
            "Module 3 - Biological Diversity",
            "Module 4 - Ecosystem Dynamics",
            "Module 5 - Heredity",
            "Module 6 - Genetic Change",
            "Module 7 - Infectious Disease",
            "Module 8 - Non-infectious Disease and Disorders"
        ]
    elif subject == "Economics":
        return [
            "All Modules",
            "Topic 1 - Introduction to Economics",
            "Topic 2 - Consumers and Business",
            "Topic 3 - Markets",
            "Topic 4 - Labour Markets",
            "Topic 5 - The Global Economy",
            "Topic 6 - Australia’s Place in the Global Economy",
            "Topic 7 - Economic Issues",
            "Topic 8 - Economic Policies and Management"
        ]
    return []

# Chatbot function for the sidebar with conversation history
def chatbot_sidebar(page_key):
    st.sidebar.header("Smart Notes Tutor")

    # Initialize conversation history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Input field for the user's question
    user_question = st.sidebar.text_input("Ask me anything!", key=f"chatbot_input_{page_key}")

    # Send button to trigger the response
    if st.sidebar.button("Ask now", key=f"send_button_{page_key}") and user_question:
        with st.spinner("Thinking..."):
            # Define chatbot flow and API request
            chatbot_url = "https://app.wordware.ai/api/released-app/9f21fcb4-daae-4529-9c1e-22e14df941b2/run"
            inputs = {"Question": user_question}
            response = do_wordware(chatbot_url, inputs)

            # Append user question and bot response to the conversation history
            st.session_state["chat_history"].append({"user": user_question, "bot": response})

    # Display the conversation history with expandable sections for each question-response pair
    st.sidebar.markdown("### Conversation History")
    for idx, chat in enumerate(st.session_state["chat_history"]):
        with st.sidebar.expander(f"Question {idx + 1}", expanded=False):
            st.markdown(f"<span style='color:blue; font-weight:bold;'>You:</span> {chat['user']}", unsafe_allow_html=True)
            st.markdown(f"<span style='color:green; font-weight:bold;'>Bot:</span> {chat['bot']}", unsafe_allow_html=True)




# Notes page
def notes_page():
    st.header("📚 Generate Study Notes")

    # Directly display the selection fields for Subject and Modules without an expander
    subject = st.selectbox("Select Subject for Notes:", ["Biology", "Economics"])
    modules = get_modules(subject)
    selected_modules = st.multiselect("Select Modules to Focus On:", modules)
    selected_modules_str = "All Modules" if "All Modules" in selected_modules else ", ".join(selected_modules)
    
    # Input for study timeframe
    time = st.text_input("Enter Study Timeframe:", placeholder="e.g., 7 Days")

    # Button to trigger notes generation
    if st.button("Generate Study Notes"):
        if not selected_modules or not time.strip():
            st.warning("Please select at least one module and enter a study timeframe before generating notes.")
        else:
            with st.spinner("Generating study notes..."):
                inputs = {"Subject": subject, "Modules": selected_modules_str, "Time": time}
                prompt_url = "https://app.wordware.ai/api/released-app/1d5dd41f-89b2-42ed-9fe3-0806eb15fab9/run"
                result = do_wordware(prompt_url, inputs)
                st.session_state["generated_notes"] = result

    # Display the generated notes
    if "generated_notes" in st.session_state and st.session_state["generated_notes"]:
        st.success("Generated Notes:")
        st.write(st.session_state["generated_notes"])
        display_topics(st.session_state["generated_notes"])

# Flashcards page with persistent generation
def flashcards_page():
    st.header("🃏 Generate Flashcards")
    
    subject = st.selectbox("Select Subject for Flashcards:", ["Biology", "Economics"])
    modules = get_modules(subject)
    selected_modules = st.multiselect("Select Modules to Focus On:", modules)
    selected_modules_str = "All Modules" if "All Modules" in selected_modules else ", ".join(selected_modules)

    if st.button("Generate Flashcards"):
        if not selected_modules:
            st.warning("Please select at least one module before generating flashcards.")
        else:
            with st.spinner("Generating flashcards..."):
                inputs = {"Subject": subject, "Modules": selected_modules_str}
                prompt_url = "https://app.wordware.ai/api/released-app/c9356c76-71a9-49af-ad56-6bb0acad1385/run"
                result = do_wordware(prompt_url, inputs)
                # Store the result in session state to prevent clearing on chatbot interaction
                st.session_state["flashcards_result"] = result

    # Check if flashcards have been generated before
    if "flashcards_result" in st.session_state:
        st.success("Generated Flashcards:")
        st.write(st.session_state["flashcards_result"])


# Practice questions page with persistent generation
def practice_questions_page():
    st.header("❓ Generate Practice Questions")
    
    subject = st.selectbox("Select Subject for Practice Questions:", ["Biology", "Economics"])
    modules = get_modules(subject)
    selected_modules = st.multiselect("Select Modules to Focus On:", modules)
    selected_modules_str = "All Modules" if "All Modules" in selected_modules else ", ".join(selected_modules)

    if st.button("Generate Practice Questions"):
        if not selected_modules:
            st.warning("Please select at least one module before generating practice questions.")
        else:
            with st.spinner("Generating practice questions..."):
                inputs = {"Subject": subject, "Modules": selected_modules_str}
                prompt_url = "https://app.wordware.ai/api/released-app/88f8c8cd-494d-48bb-aec9-c409849ecc41/run"
                result = do_wordware(prompt_url, inputs)
                # Store the result in session state to prevent clearing on chatbot interaction
                st.session_state["practice_questions_result"] = result

    # Check if practice questions have been generated before
    if "practice_questions_result" in st.session_state:
        st.success("Generated Practice Questions:")
        st.write(st.session_state["practice_questions_result"])

# Main function
def run_wordware_app():
    st.title("Smart Notes")

    # Sidebar for navigation between Notes, Flashcards, and Practice Questions pages
    if "page" not in st.session_state:
        st.session_state["page"] = "Notes"

    # Page selection dropdown
    page = st.sidebar.selectbox("Select Page", ["Notes", "Flashcards", "Practice Questions"])
    st.session_state["page"] = page

    # Divider for better separation
    st.sidebar.markdown("---")

    # Chatbot assistant section
    chatbot_sidebar(page)

    # Display the selected page content
    if st.session_state["page"] == "Notes":
        notes_page()
    elif st.session_state["page"] == "Flashcards":
        flashcards_page()
    elif st.session_state["page"] == "Practice Questions":
        practice_questions_page()

if __name__ == "__main__":
    run_wordware_app()
