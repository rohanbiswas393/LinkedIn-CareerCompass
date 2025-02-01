# CareerNinjaBot

CareerNinjaBot is an AI-powered chatbot that helps users analyze LinkedIn profiles and job postings, providing insights and recommendations. It uses Google Gemini AI for intelligent responses and Proxycurl API for LinkedIn data extraction.

## Features
- **LinkedIn Profile Analysis**: Extracts and summarizes profile details.
- **Job Posting Analysis**: Retrieves job details and provides insights.
- **AI Chatbot**: Interacts with users, answering career-related queries.
- **Streamlit UI**: Simple web-based interface for seamless interaction.

## Installation

### Prerequisites
- Python 3.8+
- A valid Proxycurl API Key
- A valid Google Gemini AI API Key

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/CareerNinjaBot.git
   cd CareerNinjaBot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up API keys:
   - Replace `self.PROXYCURL_API_KEY` in `CareerNinjaBot.py` with your Proxycurl API key.
   - Replace `genai.configure(api_key=...)` with your Gemini AI API key.
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## Usage
- Click **Profile** to analyze a LinkedIn profile.
- Click **Job** to analyze a job posting.
- Enter the LinkedIn URL and get insights.
- Use the chat interface to ask career-related questions.

## Troubleshooting
- **Invalid API Key**: Ensure your API keys are correct and active.
- **Proxycurl API Limitations**: Free tier has limitations; upgrade if necessary.
- **Streamlit Not Loading**: Run `streamlit clean` and retry.

## Contributing
Feel free to fork the repo, create a branch, and submit a pull request.

## License
MIT License. See `LICENSE` for details.

## Contact
For issues and suggestions, create a GitHub issue or contact me at [your email].

