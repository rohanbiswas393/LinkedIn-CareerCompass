import os
import time
import requests
import streamlit as st
import google.generativeai as genai
from typing import Optional, Dict, Any
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CareerNinjaBot:
    def __init__(self):
        # Hardcoded API keys (replace with your actual API keys)
        self.PROXYCURL_API_KEY = "Your_Key"
        genai.configure(api_key="Your_Key")

        # Initialize Gemini model
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            },
        )
        self.chat_session = self.model.start_chat(history=[])

        # State management
        self.current_data = {
            'profile': None,
            'job': None,
            'last_type': None
        }
        self.expecting_url = False
        self.url_type = None
        # We'll track conversation context ourselves
        self.conversation_context = []

    def scrape_linkedin_data(self, url: str, data_type: str) -> Optional[Dict[str, Any]]:
        endpoint = (
            "https://nubela.co/proxycurl/api/v2/linkedin"
            if data_type == "profile"
            else "https://nubela.co/proxycurl/api/linkedin/job"
        )
        headers = {"Authorization": f"Bearer {self.PROXYCURL_API_KEY}"}

        for attempt in range(3):
            try:
                response = requests.get(endpoint, params={"url": url}, headers=headers, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    if data_type == "profile":
                        return {
                            k: v for k, v in data.items()
                            if v not in ([], "", None)
                            and k not in ["people_also_viewed", "certifications"]
                        }
                    else:
                        return data
            except Exception:
                pass
            time.sleep(2 * (attempt + 1))
        return None

    def format_data(self, data: Dict, data_type: str) -> str:
        if not data:
            return f"❌ Failed to retrieve {data_type} data. Please check the URL and try again."

        try:
            if data_type == "profile":
                return f"""✅ **Profile Analysis Complete**

👤 Name: {data.get('full_name', 'N/A')}
📌 Headline: {data.get('headline', 'N/A')}
🌍 Location: {data.get('country', 'N/A')}
💼 Experience: {len(data.get('experiences', []))} positions
🔧 Skills: {', '.join(data.get('skills', [])[:10]) if data.get('skills') else 'N/A'}
📚 About: {data.get('summary', 'N/A')}"""
            else:
                return f"""✅ **Job Posting Analysis**

📌 Title: {data.get('job_title', 'N/A')}
🏢 Company: {data.get('company', {}).get('name', 'N/A')}
📍 Location: {data.get('location', {}).get('city', 'N/A')}, {data.get('location', {}).get('country', 'N/A')}
📅 Posted: {data.get('posting_date', 'N/A')}
👥 Applicants: {data.get('applicant_count', 'N/A')}
📝 Description: {data.get('job_description', '')[:250]}..."""
        except Exception as e:
            return f"Error formatting {data_type} data: {str(e)}"

    def handle_message(self, user_input: str) -> str:
        user_input = user_input.strip().lower()
        if user_input in ["exit", "quit"]:
            return "exit"

        if self.expecting_url:
            return self._process_url_input(user_input)

        if user_input in ["profile", "linkedin profile"]:
            self.expecting_url = True
            self.url_type = "profile"
            return "Please enter your LinkedIn profile URL:"
        elif user_input in ["job", "job posting"]:
            self.expecting_url = True
            self.url_type = "job"
            return "Please enter the LinkedIn job URL:"

        return self._handle_chat_with_context(user_input)

    def _process_url_input(self, url: str) -> str:
        try:
            data = self.scrape_linkedin_data(url, self.url_type)
            if not data:
                self.expecting_url = False
                return f"❌ Failed to retrieve {self.url_type} data. Please check the URL and try again."

            self.current_data[self.url_type] = data
            self.current_data['last_type'] = self.url_type
            formatted_data = self.format_data(data, self.url_type)

            context_prompt = (
                f"Context: Analyzing {self.url_type} data for "
                f"{data.get('full_name', '') if self.url_type == 'profile' else data.get('job_title', '')}"
            )
            self.chat_session.send_message(context_prompt)

            self.expecting_url = False
            return (
                f"{formatted_data}\n\n"
                f"You can now ask questions about this {self.url_type} or continue with other queries!"
            )
        except Exception as e:
            self.expecting_url = False
            return f"⚠️ Error processing URL: {str(e)}"

    def _handle_chat_with_context(self, message: str) -> str:
        try:
            data_context = self._get_current_data_context()
            chat_history = "\n".join(
                [f"User: {entry['user']}\nAssistant: {entry['response']}"
                 for entry in self.conversation_context[-4:]]
            )
            full_prompt = f"""
{data_context}

Conversation History:
{chat_history}

New User Message: {message}

Provide a helpful response considering both the current context and previous conversation.
"""
            response = self.chat_session.send_message(full_prompt).text
            self.conversation_context.append({'user': message, 'response': response})
            self.conversation_context = self.conversation_context[-4:]
            return response
        except Exception as e:
            return f"⚠️ Chat error: {str(e)}"

    def _get_current_data_context(self) -> str:
        if not self.current_data['last_type']:
            return ""
        data_type = self.current_data['last_type']
        data = self.current_data[data_type]
        if data_type == 'profile':
            return (
                f"Current Profile Context:\n"
                f"Name: {data.get('full_name', 'N/A')}\n"
                f"Headline: {data.get('headline', 'N/A')}\n"
                f"Summary: {data.get('summary', 'N/A')[:200]}"
            )
        else:
            return (
                f"Current Job Context:\n"
                f"Title: {data.get('job_title', 'N/A')}\n"
                f"Company: {data.get('company', {}).get('name', 'N/A')}\n"
                f"Description: {data.get('job_description', 'N/A')[:200]}"
            )


def run_streamlit_app():
    st.title("CareerNinja: Streamlit UI")
    st.write("Analyze LinkedIn profiles or job postings, and chat about them in real time!")

    if "bot" not in st.session_state:
        st.session_state["bot"] = CareerNinjaBot()
    bot = st.session_state["bot"]

    st.subheader("Data Retrieval")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Profile"):
            bot.expecting_url = True
            bot.url_type = "profile"
    with col2:
        if st.button("Job"):
            bot.expecting_url = True
            bot.url_type = "job"

    if bot.expecting_url:
        st.info(f"Please enter your LinkedIn {bot.url_type} URL:")
        url_input = st.text_input("LinkedIn URL", key="url_input")
        if url_input:
            response = bot.handle_message(url_input)
            st.success(response)

    st.subheader("Chat Interface")
    user_chat_input = st.text_input("Type your message here:", key="user_chat_input")
    if st.button("Send"):
        if user_chat_input:
            response = bot.handle_message(user_chat_input)
            if response == "exit":
                st.write("Exiting chat. Restart the app to begin a new session.")
            else:
                st.write("CareerNinja:", response)

    if bot.conversation_context:
        st.subheader("Conversation History")
        for idx, item in enumerate(bot.conversation_context):
            st.markdown(f"**User**: {item['user']}")
            st.markdown(f"**Assistant**: {item['response']}")


def main():
    run_streamlit_app()

if __name__ == "__main__":
    main()