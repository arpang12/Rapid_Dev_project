# System Patterns

## System Architecture
The system will consist of a Python script that utilizes the Reddit API to gather data and generate personas. The script will be organized into modules for data gathering, persona generation, and output formatting.

## Key Technical Decisions
*   Using the Reddit API for data gathering.
*   Using Python for scripting.
*   Using Markdown for documentation.

## Design Patterns in Use
*   Modular design for code organization.
*   Data-driven approach for persona generation.
*   Agent-based approach for sentiment analysis and persona mapping.
*   Streamlit UI for user interaction.

## Component Relationships
*   The data gathering module will provide data to the persona generation module.
*   The persona generation module will provide personas to the output formatting module.
*   The sentiment analysis agent will analyze the subreddit comments and provide sentiment analysis.
*   The persona mapping agent will create a persona map based on the subreddit comments.
*   The Streamlit UI will allow users to input parameters and view the output.

## Critical Implementation Paths
*   Gathering data from the Reddit API.
*   Generating realistic personas based on the gathered data.
*   Formatting the generated personas for output.
