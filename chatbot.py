from __future__ import annotations
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from typing import Iterable
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
import time

# class Seafoam(Base):
#     def __init__(
#         self,
#         *,
#         primary_hue: colors.Color | str = colors.emerald,
#         secondary_hue: colors.Color | str = colors.blue,
#         neutral_hue: colors.Color | str = colors.gray,
#         spacing_size: sizes.Size | str = sizes.spacing_md,
#         radius_size: sizes.Size | str = sizes.radius_md,
#         text_size: sizes.Size | str = sizes.text_lg,
#         font: fonts.Font
#         | str
#         | Iterable[fonts.Font | str] = (
#             fonts.GoogleFont("Quicksand"),
#             "ui-sans-serif",
#             "sans-serif",
#         ),
#         font_mono: fonts.Font
#         | str
#         | Iterable[fonts.Font | str] = (
#             fonts.GoogleFont("IBM Plex Mono"),
#             "ui-monospace",
#             "monospace",
#         ),
#     ):
#         super().__init__(
#             primary_hue=primary_hue,
#             secondary_hue=secondary_hue,
#             neutral_hue=neutral_hue,
#             spacing_size=spacing_size,
#             radius_size=radius_size,
#             text_size=text_size,
#             font=font,
#             font_mono=font_mono,
#         )

# seafoam = Seafoam()

import os
os.environ["OPENAI_API_KEY"] = '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'

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0,model_name="gpt-4")

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader

reports_dir = 'C:\\Users\\ericy\\Desktop\\WashUChatBuddy\\WashU-Chat-Buddy\\Reports'

pdf_loader = DirectoryLoader(reports_dir, glob="**/*.pdf")
txt_loader = DirectoryLoader(reports_dir, glob="**/*.txt")
csv_loader = CSVLoader(
    file_path=reports_dir + "\\student_events.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ["Event Title", "Organization", "Location", "Date/Time"],
    },
)
csv_loader1 = CSVLoader(
    file_path="./Reports/webstac_ARTSCI_FINAL.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ["Course ID", "Course Title", "Course Credits", "Section", "Day", "Time", "Building", "Instructor"],
    }
)

loaders = [pdf_loader, txt_loader, csv_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())

#print(f"Total number of documents: {len(documents)}")

text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), return_source_documents=True)

css = """
* {
    font-family: 'Source Sans 3', sans-serif;
    font-color: black;
}
#warning {
    background-color: #a51417
}
.feedback textarea {
    font-size: 24px !important;
    font-color: black;
}
.gradio-container {
    background-image: url(file=WashuBuddyLogo.png);
    height: auto;
    max-width: 100%;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center bottom;
}
.gradio-container::before {
    content: "";
    background: rgba(0, 0, 0, 0.1);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
}
"""

demo = gr.Blocks(css=css)

# Define chat interface
with demo:
    chatbot = gr.Chatbot(elem_id="warning", elem_classes="feedback")
    msg = gr.Textbox(label="How may I help you?", elem_id="warning", elem_classes="feedback")
    clear = gr.Button("Clear")
    chat_history = []

    def user(query, chat_history):
        print("User query:", query)
        print("Chat history:", chat_history)

        # Convert chat history to list of tuples
        chat_history_tuples = []
        for message in chat_history:
            chat_history_tuples.append((message[0], message[1]))

        # Get result from QA chain
        result = qa({"question": query, "chat_history": chat_history_tuples})

        # Append user message and response to chat history
        chat_history.append((query, result["answer"]))
        print("Updated chat history:", chat_history)

        # Return a new Textbox object instead of using update
        return gr.Textbox(value=""), chat_history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(debug=True, share=True)