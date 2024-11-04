import g4f
import streamlit as st
import fitz  # PyMuPDF for PDF files
from docx import Document  # For reading Word files

# Page configuration
st.set_page_config(
    page_title="NBFS Chat App",
    page_icon="💬",
    layout="centered"
)

# App title
st.title('FADAI Chat 💬')

# CSS for styling chats
st.markdown("""
    <style>
        .chat-bubble-user {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: left;
            max-width: 70%;
            word-wrap: break-word;
        }
        .chat-bubble-bot {
            background-color: #E1E1E1;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
            max-width: 70%;
            word-wrap: break-word;
        }
        .input-section {
            display: flex;
            align-items: center;
            margin-top: 20px;
        }
        .file-upload {
            margin-right: 10px;
        }
        .btn-send {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn-send:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Session state variables to store questions and responses
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'file_text' not in st.session_state:
    st.session_state.file_text = ""

# Display chat history
def display_chat_history():
    if st.session_state.questions:
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f'<div class="chat-bubble-user">{question}</div>', unsafe_allow_html=True)
            if i < len(st.session_state.responses):
                st.markdown(f'<div class="chat-bubble-bot">{st.session_state.responses[i]}</div>', unsafe_allow_html=True)

# Display chat history
display_chat_history()

# New question input section with send button
st.markdown('<div class="input-section">', unsafe_allow_html=True)
new_question = st.text_area('Enter your new question', key=f"new_question_{len(st.session_state.questions)}")
if st.button('Send Question', key="send_btn", help="Send question"):
    if new_question:
        st.session_state.questions.append(new_question)
        try:
            response = g4f.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{"role": "user", "content": new_question}],
                stream=True
            )
            response_text = "".join(response)
            st.session_state.responses.append(response_text)
        except Exception as e:
            st.error("An issue occurred while receiving a response from the model.")
            st.error(str(e))
st.markdown('</div>', unsafe_allow_html=True)

# File upload
st.markdown('<div class="input-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx"], key="file_upload", help="Upload your file (Word or PDF)")
st.markdown('</div>', unsafe_allow_html=True)

# Functions to extract text from files
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")
        return text
    except Exception as e:
        st.error("An error occurred while processing the PDF file.")
        st.error(str(e))
        return ""

def extract_text_from_word(docx_file):
    try:
        doc = Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error("An error occurred while processing the Word file.")
        st.error(str(e))
        return ""

# Process uploaded file
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'pdf':
        st.session_state.file_text = extract_text_from_pdf(uploaded_file)
    elif file_type == 'docx':
        st.session_state.file_text = extract_text_from_word(uploaded_file)
    st.text_area("File Text:", st.session_state.file_text, height=200)

# Ask questions from file text
if st.session_state.file_text:
    file_question = st.text_area('Ask a question from file text', key=f"file_question_{len(st.session_state.questions)}")
    if st.button('Ask Question from File', key="file_question_btn"):
        if file_question:
            full_content = f"File Text: {st.session_state.file_text}\nQuestion: {file_question}"
            st.session_state.questions.append(file_question)
            try:
                response = g4f.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": full_content}],
                    stream=True
                )
                response_text = "".join(response)
                st.session_state.responses.append(response_text)
            except Exception as e:
                st.error("An issue occurred while receiving a response from the model.")
                st.error(str(e))