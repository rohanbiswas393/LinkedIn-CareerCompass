CareerNinjaBot

CareerNinjaBot is an AI-powered career assistant that allows users to analyze LinkedIn profiles and job postings using the Proxycurl API. It also provides an interactive chat interface using Google's Gemini model to discuss career insights and job market trends.

Features

Fetch LinkedIn profile details (Name, Headline, Experience, Skills, Summary, etc.).

Fetch LinkedIn job posting details (Title, Company, Location, Applicants, Description, etc.).

AI-powered chat interface to discuss career-related queries based on retrieved data.

Streamlit UI for an intuitive user experience.

Installation & Setup

Prerequisites

Ensure you have Python installed (preferably Python 3.8+).

Clone the Repository

git clone https://github.com/rohanbiswas393/CareerNinjaBot.git
cd CareerNinjaBot

Install Dependencies

Use the provided requirements.txt to install necessary Python packages:

pip install -r requirements.txt

API Key Configuration

Proxycurl API Key (For LinkedIn Scraping)

You need an API key from Proxycurl.

Replace the PROXYCURL_API_KEY in CareerNinjaBot class:

self.PROXYCURL_API_KEY = "your_proxycurl_api_key_here"

Google Gemini API Key

Get an API key from Google AI.

Replace the api_key in the genai.configure function:

genai.configure(api_key="your_google_gemini_api_key_here")

Running the Application

Run the Streamlit app with:

streamlit run main.py

This will start a local server where you can interact with the bot via the Streamlit UI.

Usage

Profile Analysis

Click on the "Profile" button.

Enter the LinkedIn profile URL.

The bot will fetch and display the profile details.

You can then chat with the bot to discuss career insights based on the retrieved data.

Job Posting Analysis

Click on the "Job" button.

Enter the LinkedIn job URL.

The bot will fetch and display job posting details.

Chat with the bot to discuss job opportunities and insights.

Chat Interface

Enter any career-related question in the chat input.

The bot will provide responses based on retrieved data and general career insights.

Conversation history is displayed within the Streamlit UI.

Troubleshooting

If API requests fail, ensure that your API keys are correctly configured.

If the application does not start, verify that dependencies are installed correctly.

If the chat does not respond, check the Google Gemini API key validity.

Contribution

Feel free to fork and contribute to the repository by submitting pull requests. For major changes, please open an issue first to discuss your ideas.

License

This project is licensed under the MIT License.

Contact

For queries, contact Rohan Biswas.

