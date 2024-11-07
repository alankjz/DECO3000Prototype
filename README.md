# Smart Notes AI

**Smart Notes AI** is an AI-powered study assistant that helps students generate personalised study notes, flashcards, and practice questions based on selected topics. It includes an interactive chatbot for instant support and further information retrieval.

## Features
- Generate topic-based **Study Notes**.
- Create **Flashcards** for quick revision.
- Generate **Practice Questions** based on selected topics.
- Interactive **chatbot** that provides additional information and supports students in real-time.

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup Instructions
1. Clone this repository or download as Zip File:
   ```bash
   git clone https://github.com/alankjz/DECO3000Prototype
   ```
2. Navigate into the project directory in terminal:
   ```bash
   cd DECO3000Prototype-main
   ```
3. Install required packages:
   ```bash
   pip install streamlit 
   pip install requests 
   pip install python-dotenv
   ```
4. Create a `.env` file in the root directory and add your API key:
   ```plaintext
   API_KEY='your_api_key_here'
   ```
5. Run the app:
   ```bash
   Make sure interpreter is in Python 3.12.4 ('base') 
   Run the app in the app.py terminal with: 

   streamlit run app.py 
   ```
6. Access Wordware.ai URL (If not working)
   ```bash
   Refer to Wordware file links if any errors

   Smart Notes: https://app.wordware.ai/explore/apps/1d5dd41f-89b2-42ed-9fe3-0806eb15fab9
   Practise Questions: https://app.wordware.ai/explore/apps/88f8c8cd-494d-48bb-aec9-c409849ecc41
   Flash Cards: https://app.wordware.ai/explore/apps/c9356c76-71a9-49af-ad56-6bb0acad1385
   Extract Modules: https://app.wordware.ai/explore/apps/18e4b7f4-57f4-4b41-9797-90eebff79ebf
   Chat Bot: https://app.wordware.ai/explore/apps/9f21fcb4-daae-4529-9c1e-22e14df941b2
   
   ```


## Usage
- Choose a subject and modules for note generation.
- Generate flashcards and practice questions as study aids.
- Use the chatbot to ask questions and get additional whenever you want when making your notes, flashcards or practise questions.


## Acknowledgments / AI Tools and Libraries Used
- **Streamlit**: Interactive UI for easy accessibility and user interaction.
- **OpenAI/Wordware API**: For AI-driven content generation and chatbot functionality.

