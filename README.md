# WashU Chat Buddy

## Overview
WashU Chat Buddy is a chatbot designed to assist Washington University (WashU) students with class scheduling. It's trained on a dataset that includes WUGO events, course listings, and more. You can access it at www.washubuddy.com.

## Repository Structure

- **Reports Folder**: Contains all forms of data used to load into the Langchain DocumentLoader.

- **Webscraper**: This directory includes the source code for various scraping tasks:
    1. PDF to text converter
    2. Student events scraper
    3. Course descriptions scraper from WUSTL course listing

- **chatbot.py**: This is the main Gradio application used to create the chatbot. It handles the loading of the frontend and backend, and creates a local host.

## Deprecated Instructions

### Running the Chatbot Locally

If you want to run the chatbot on your local environment, follow these steps:

1. Navigate to the project path with `cd [project-path]`.
2. Replace the placeholder in the code with your OpenAI API key.
3. Run the Gradio chatbot with `python chatbot.py`.
4. Access the chatbot at http://127.0.0.1:7860/.
