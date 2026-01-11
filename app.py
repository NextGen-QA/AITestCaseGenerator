## Section 1 - Import all libraries
import streamlit as st
from jira import JIRA
from openai import OpenAI
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import json


## Load env files
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Test Generator",
    page_icon="🤖",
    layout="wide"

)

#Main title
st.title("🤖 AI Test Generator")
st.write("Generate test cases from Jira user stories using AI")

# Sidebar for Configuration
st.sidebar.header("⚙️ Configuration")
st.sidebar.write("Enter your credentials below")
st.sidebar.subheader("Jira Credentials")

# Input field for Jira URL
jira_url = st.sidebar.text_input(
    "Jira URL",
    value=os.getenv("JIRA_URL", ""),
    placeholder="https://your-domain.atlassian.net",
    help="Enter your Jira instance URL"
)

#Email
jira_email = st.sidebar.text_input(
    "Jira Email",
    value=os.getenv("JIRA_EMAIL", ""),
    placeholder="your-email@example.com",
    help="Enter your Jira account email"
)

# Input field for Jira API token
jira_token = st.sidebar.text_input(
    "Jira API Token",
    value=os.getenv("JIRA_API_TOKEN", ""),
    type="password",
    placeholder="Enter your API token",
    help="Enter your Jira API token"
)

# Sidebar divider
st.sidebar.divider()


# Input field for OpenAI API key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
    placeholder="sk-...",
    help="Enter your OpenAI API key"
)

# Create a divider
st.divider()

# Section 1: Project Selection
st.header("1️⃣ Select Jira Project")

#Button to fetch Jira projects
if st.button("Fetch Project",type="primary"):
     if not jira_url or not jira_token or not jira_email:
         st.error("Please enter all the Jira credentials")
     else:
        try:
            with st.spinner("Connecting to Jira"):
                #Connecting to Jira
                jira_connection = JIRA(server=jira_url,basic_auth=(jira_email,jira_token))
                projects = jira_connection.projects()

                ## Store projects in session
                st.session_state.projects = projects
                st.session_state.jira_connection = jira_connection
                st.success("Successfully fetched Jira projects")
        except Exception as error:
            st.error("Error connecting to Jira")

            
 
# Display project selection dropdown if projects are available
if 'projects' in st.session_state:
    # Create a list of project names and keys
    project_options = [f"{project.key} - {project.name}" for project in st.session_state.projects]

    # Dropdown to select a project
    selected_project = st.selectbox(
        "Select a Project",
        options=project_options,
        help="Choose the project from which to fetch user stories"
    )

# Extract User stories from a particular Jira project
    if selected_project:
        project_key = selected_project.split(" - ")[0]
        st.info(f"Selected Project Key: {project_key}")

        # Create a divider
        st.divider()

        # Section 2: Fetch User Stories
        st.header("2️⃣ Fetch User Stories")

        #Button to fetch the user stories
        if st.button("Fetch User Stories", type="primary"):
            try:
                with st.spinner("Fetching Jira user stories"):
                    jql_query = f'project = {project_key} AND issuetype = Story'
                    # Fetch issues using JQL
                    issues = st.session_state.jira_connection.search_issues(jql_query, maxResults=50)

                    # Store issues in session state
                    st.session_state.issues = issues
                    st.success(f"Successfully fetched {len(issues)} user stories!")
            except Exception as error:
                st.error("Error fetching the user stories")

    # Display user stories if available
    if 'issues' in st.session_state:
        st.subheader("User Stories")

        #Create a list to store user story data
        user_stories_data = []

       # Loop through each issue
        for issue in st.session_state.issues:
                # Get issue key
             issue_key = issue.key

                # Get issue summary
             issue_summary = issue.fields.summary

                # Get issue description (handle None)
             issue_description = issue.fields.description if issue.fields.description else "No description"

                # Add to list
             user_stories_data.append({
                    "Key": issue_key,
                    "Summary": issue_summary,
                    "Description": issue_description
                })
             
        #Create a dataframe to display user story
        user_stories_df = pd.DataFrame(user_stories_data)

        ## Display the above dataframe
        st.dataframe(user_stories_df,use_container_width=True)
        st.divider()

        # Create a list of options for selection
        story_options = []
        for story in user_stories_data:
            option_text = f"{story['Key']} - {story['Summary']}"
            story_options.append(option_text)

        #Multiselect Option widget
        selected_stories = st.multiselect("" \
            "Select multiple stories", options = story_options,
            default=story_options,
            help="Select one or more user stories to generate your test cases")
        
        st.info(f"Selected {len(selected_stories)} out of {len(story_options)} user stories")

         # Create a divider
        st.divider()

        
        #Generate Test Cases
        st.header("Generate Test Cases")
        if st.button("Generate Test Cases with AI", type="primary"):
                # Check if any stories are selected
                if len(selected_stories) == 0:
                    st.error("Please select at least one user story!")
                elif not openai_api_key:
                    st.error("Please enter your OpenAI API key first!")
                else:
                    try:
                        # Show a spinner while generating test cases
                        with st.spinner("Generating test cases using AI... This may take a few minutes."):
                            openai_client = OpenAI(api_key=openai_api_key)
                            
                            #List to store all the test cases
                            all_test_cases = []

                            #Progress Bar
                            progress_bar = st.progress(0)

                            # Extract selected issue keys from the selected stories
                            selected_keys = []
                            for selected in selected_stories:
                                # Extract the key (format is "KEY - Summary")
                                key = selected.split(" - ")[0]
                                selected_keys.append(key)

                            # Filter issues to only include selected ones
                            selected_issues = []
                            for issue in st.session_state.issues:
                                if issue.key in selected_keys:
                                    selected_issues.append(issue)


                            # Loop through each selected user story
                            for index, issue in enumerate(selected_issues):
                                # Get issue details
                                issue_key = issue.key
                                issue_summary = issue.fields.summary
                                issue_description = issue.fields.description if issue.fields.description else "No description"

                                #Create Open AI Prompt
                                prompt = f"""You are a QA engineer. Generate comprehensive test cases for the following user story.

User Story ID: {issue_key}
Summary: {issue_summary}
Description: {issue_description}

Generate 5-7 test cases and return them as a JSON array. Each test case should have:
- test_case_id: A unique ID (e.g., TC001, TC002)
- test_case_title: A clear title
- test_steps: Detailed steps to execute the test (as a single string with numbered steps)
- expected_result: The expected outcome
- priority: Priority level (High/Medium/Low)
- type: Type of test (Functional/UI/Integration/etc)

Return ONLY the JSON array, no additional text."""
                                
                                # Call OpenAI API
                                response = openai_client.chat.completions.create(
                                    model="gpt-4",
                                    messages=[
                                        {"role": "system", "content": "You are a helpful QA engineer who creates detailed test cases. Always respond with valid JSON only."},
                                        {"role": "user", "content": prompt}
                                    ],
                                    temperature=0.7
                                )
                                # Get the generated test cases
                                generated_text = response.choices[0].message.content

                                #Parse Json Response
                                try:
                                    # Remove markdown code blocks if present
                                    if "```json" in generated_text:
                                        generated_text = generated_text.split("```json")[1].split("```")[0].strip()
                                    elif "```" in generated_text:
                                        generated_text = generated_text.split("```")[1].split("```")[0].strip()

                                    test_cases_json = json.loads(generated_text)

                                # Add each test case as a separate row
                                    for tc in test_cases_json:
                                        all_test_cases.append({
                                            "User Story Key": issue_key,
                                            "User Story Summary": issue_summary,
                                            "User Story Description": issue_description,
                                            "Test Case ID": tc.get("test_case_id", ""),
                                            "Test Case Title": tc.get("test_case_title", ""),
                                            "Test Steps": tc.get("test_steps", ""),
                                            "Expected Result": tc.get("expected_result", ""),
                                            "Priority": tc.get("priority", ""),
                                            "Type": tc.get("type", "")
                                        })
                                except json.JSONDecodeError:
                                    # Fallback: If JSON parsing fails, store as text
                                    all_test_cases.append({
                                        "User Story Key": issue_key,
                                        "User Story Summary": issue_summary,
                                        "User Story Description": issue_description,
                                        "Test Case ID": "",
                                        "Test Case Title": "",
                                        "Test Steps": generated_text,
                                        "Expected Result": "",
                                        "Priority": "",
                                        "Type": ""
                                    })
                                
                                # Update progress bar
                                progress_value = (index + 1) / len(selected_issues)
                                progress_bar.progress(progress_value)
                            
                            # Store test cases in session state
                            st.session_state.test_cases = all_test_cases

                            st.success("Test cases generated successfully!")
                    except Exception as error:
                        st.error("Error in generating test cases")


        #Display generated test cases if they are available
        if 'test_cases' in st.session_state:
            st.divider()
            st.header("Generated test cases")
            # Create DataFrame to display all test cases
            test_cases_df = pd.DataFrame(st.session_state.test_cases)

            # Check if the test cases have the structured format
            required_columns = ['Test Case ID', 'Test Case Title', 'Test Steps', 'Expected Result', 'Priority', 'Type']

            has_format = all(col in test_cases_df.columns for col in required_columns)
            if not has_format:
                st.warning("Test cases are not present in correct format")
                if st.button("Clear Old Test Cases"):
                        del st.session_state.test_cases
                        st.rerun()
            else:
                unique_stories = test_cases_df['User Story Key'].unique()

                for story_key in unique_stories:
                        # Filter test cases for this user story
                        story_test_cases = test_cases_df[test_cases_df['User Story Key'] == story_key]

                        # Get the summary for the expander title
                        story_summary = story_test_cases.iloc[0]['User Story Summary']

                        # Create an expander for each user story
                        with st.expander(f"{story_key}: {story_summary} ({len(story_test_cases)} test cases)"):
                            # Display test cases in a table
                            display_df = story_test_cases[['Test Case ID', 'Test Case Title', 'Test Steps', 'Expected Result', 'Priority', 'Type']]
                            st.dataframe(display_df, use_container_width=True, hide_index=True)

                # Create a divider
                st.divider()
                
                #Download Test Cases
                
                st.header("Download Test Cases")
                # Create DataFrame for CSV download
                test_cases_df = pd.DataFrame(st.session_state.test_cases)

                # Convert DataFrame to CSV
                csv_data = test_cases_df.to_csv(index=False)

                # Create timestamp for filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_cases_{timestamp}.csv"

                # Download button
                st.download_button(
                    label="Download Test Cases as CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    type="primary"
                )

# Footer
st.divider()
st.caption("AI Test Generator - Powered by OpenAI GPT-4 and Streamlit")