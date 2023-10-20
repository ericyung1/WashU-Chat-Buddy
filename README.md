# WashU Chat Buddy

How to run on your local environment
1) cd into project path
2) Change the Openai api key
3) run gradio chatbot.py
4) Go to port http://127.0.0.1:7860/

Purpose:
Create a chatbot catered to help WashU students schedule classes. Trained with data that includes WUGO events, course listings, etc.

Reports Folder:<br>
All forms of data used to load into Langchain DocumentLoader

Webscraper:<br>
1) Source Code for pdf to txt converter
2) Source Code for student events
3) Source Code for scraping course descriptions from WUSTL course listing

chatbot.py - main Gradio application used to create chatbot, load frontend/backend, and create local host
