# AI Test Generator

An intelligent test case generation tool that leverages OpenAI GPT-4 to automatically create comprehensive test cases from Jira user stories.

## Overview

AI Test Generator is a Streamlit-based web application that streamlines the QA process by automatically generating detailed test cases from Jira user stories. It connects to your Jira instance, fetches user stories, and uses AI to create structured, comprehensive test cases that can be exported as CSV files.

## Features

- **Jira Integration**: Connect to your Jira instance and fetch projects and user stories
- **AI-Powered Test Generation**: Automatically generate 5-7 test cases per user story using OpenAI GPT-4
- **Multi-Story Selection**: Select one or multiple user stories for batch test case generation
- **Structured Test Cases**: Each test case includes:
  - Unique Test Case ID
  - Test Case Title
  - Detailed Test Steps
  - Expected Results
  - Priority Level (High/Medium/Low)
  - Test Type (Functional/UI/Integration/etc.)
- **Export Functionality**: Download generated test cases as CSV files with timestamps
- **User-Friendly Interface**: Clean, intuitive Streamlit interface with progress tracking

## Prerequisites

- Python 3.8 or higher
- Jira account with API access
- OpenAI API key with GPT-4 access
- Jira API token

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AITestGenerator
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with your credentials:
```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
OPENAI_API_KEY=sk-your-openai-api-key
```

## Configuration

### Getting Jira API Token

1. Log in to your Atlassian account
2. Go to Account Settings > Security > API Tokens
3. Click "Create API token"
4. Give it a label and copy the generated token

### Getting OpenAI API Key

1. Sign up or log in to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new API key
4. Copy and store it securely

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. The application will open in your default web browser at `http://localhost:8501`

3. Enter your credentials in the sidebar:
   - Jira URL
   - Jira Email
   - Jira API Token
   - OpenAI API Key

4. Follow the workflow:
   - **Step 1**: Click "Fetch Project" to retrieve your Jira projects
   - **Step 2**: Select a project from the dropdown
   - **Step 3**: Click "Fetch User Stories" to load stories from the selected project
   - **Step 4**: Select one or more user stories from the list
   - **Step 5**: Click "Generate Test Cases with AI" to create test cases
   - **Step 6**: Review the generated test cases
   - **Step 7**: Download test cases as CSV

## Dependencies

- **streamlit**: Web application framework
- **jira**: Jira API client
- **openai**: OpenAI API client for GPT-4 integration
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation and CSV export

## Project Structure

```
AITestGenerator/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in version control)
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
└── venv/                 # Virtual environment (not in version control)
```

## Output Format

Generated test cases include the following fields:
- **User Story Key**: Jira issue key
- **User Story Summary**: Brief description of the user story
- **User Story Description**: Detailed user story description
- **Test Case ID**: Unique identifier (TC001, TC002, etc.)
- **Test Case Title**: Descriptive title for the test case
- **Test Steps**: Numbered steps to execute the test
- **Expected Result**: Expected outcome of the test
- **Priority**: Test priority level
- **Type**: Category of test

## Limitations

- Maximum of 50 user stories fetched per project (can be modified in code)
- Uses GPT-4 model (ensure your OpenAI account has access)
- Requires active internet connection for API calls
- API rate limits apply based on your OpenAI plan

## Troubleshooting

### Connection Issues
- Verify your Jira URL format: `https://your-domain.atlassian.net`
- Ensure your API token is valid and not expired
- Check your network connection and firewall settings

### API Errors
- Confirm OpenAI API key is valid and has GPT-4 access
- Check your OpenAI account has sufficient credits
- Review API rate limits on your OpenAI plan

### No User Stories Found
- Verify the selected project contains user stories
- Check that stories are of type "Story" in Jira
- Ensure you have permissions to view the stories

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or suggestions, please create an issue in the repository.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT-4](https://openai.com/)
- Integrates with [Atlassian Jira](https://www.atlassian.com/software/jira)
