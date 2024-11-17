import streamlit as st
from groq import Groq
import speech_recognition as sr  # Speech recognition library

# Function to draft messages
def draft_message(content, role='user'):
    return {
        "role": role,
        "content": content
    }

# API Key for Groq Client
api_key = "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"
client = Groq(api_key=api_key)

# CSS Styling
css = """
<style>
    .response-box {
        padding: 10px;
        background-color: #f9f9f9;
        border-left: 5px solid #66bb6a;
        margin-top: 10px;
    }
    #speech-btn {
        background-color: #66bb6a;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    h1 {
        text-align: center;
        color: #66bb6a;
    }
    p {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
    }
    input[type="text"] {
        padding: 10px;
        font-size: 1rem;
        width: 70%;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    button {
        padding: 10px 20px;
        font-size: 1rem;
        background-color: #66bb6a;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
"""

# HTML for Speech Input Integration
speech_recognition_html = """
<script>
    const input = document.getElementById("speech-input");
    const startButton = document.getElementById("start-speech");

    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;

        startButton.addEventListener('click', () => {
            recognition.start();
        });

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            input.value = transcript;
        };

        recognition.onerror = function(event) {
            alert('Error occurred in recognition: ' + event.error);
        };
    } else {
        alert("Your browser does not support speech recognition. Please use Google Chrome.");
    }
</script>
"""

# Streamlit HTML and Speech Button
html = """
<h1>🌿 GreenShield AI</h1>
<p style="text-align: center; font-size: 1.2rem;">How can GreenShield AI Help you today?</p>
<div style="display: flex; gap: 10px; justify-content: center; align-items: center;">
    <input id="speech-input" type="text" placeholder="Type or speak your query here..." style="padding: 10px; font-size: 1rem; width: 70%;">
    <button id="start-speech" style="padding: 10px 20px; font-size: 1rem; background-color: #66bb6a; color: white; border: none; border-radius: 5px;">🎤 Speak</button>
</div>
"""

# Inject HTML, CSS, and JavaScript
st.markdown(css, unsafe_allow_html=True)
st.markdown(html + speech_recognition_html, unsafe_allow_html=True)

# Speech recognition functionality using SpeechRecognition library
recognizer = sr.Recognizer()

def recognize_speech():
    """Handles speech recognition using the microphone."""
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("Audio received! Processing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            st.error("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    return ""

# Function to draft messages
def draft_message(content, role='user'):
    return {
        "role": role,
        "content": content
    }

# User input handling
user_prompt = st.text_input("Or type your prompt here:", placeholder="Your query will appear here...")

if st.button("🎤 Speak"):
    user_prompt = recognize_speech()  # Update the input field with speech

if st.button("Get Response"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful environmentalist assistant which can and should answer queries through "
                        "a broader perspective. Your mission is to inform the user about environmentalism and respond "
                        "to their queries in the language of their prompt. If the user query does not have much to do "
                        "with environmentalism then you should still be able to answer their query."
                    ),
                },
                draft_message(user_prompt)
            ]

            try:
                chat_completion = client.chat.completions.create(
                    temperature=1.0,
                    n=1,
                    model="mixtral-8x7b-32768",
                    max_tokens=10000,
                    messages=messages
                )

                response = chat_completion.choices[0].message.content
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)
                st.info(f"Total Tokens Used: {chat_completion.usage.total_tokens}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt.")
