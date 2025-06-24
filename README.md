# 🧠 Summarizerbot - An LLM-Powered Document Summarizer, Searcher, and Chatbot
A modular AI-powered agent built in Python that, given a directory with documents:

- Performs extractive and abstractive summarization on the documents, with customizable length.
- Enables you to look up your documents by content (i.e. you say what you're looking for and the agent will tell you 
 the files that best match your query)
- Supports interactive chat about the documents' content, so you'll be able to make the most of your stored knowledge.

This application is written in Python with, mainly, the Langchain and Gradio frameworks.

---

## 📚 Features

- 🔍 **Semantic Search** – Find files based on their content using natural language queries.
- 📝 **Extractive Summarization** – Get the most relevant sentences from your document.
- 🧠 **Abstractive Summarization** – Get a summary of your document that doesn't necessarily use the same words as it.
- 💬 **AI Assistant Chat** – Have a chat with an AI assistant you can ask about the content of your documents.
- ♻  **Real-Time Vector DB Sync** – Auto-detects added, deleted, or modified files and updates the underlying 
 vector database, as often as you want.
- 📂 **Multi-format Support** – Handles `.txt`, `.pdf`, and `.docx` files.

---

## 🛠️ Tech Stack

- **Python 3.11+**
- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [Gradio](https://gradio.app/)
- [Chroma Vector DB](https://docs.trychroma.com/)
- `PyMuPDF`, `Unstructured`, `TextLoader`, `configparser`, `logging`, etc.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```


### 2. Configure environment
Create a `config.ini` file if it didn't exist in the same directory summarizerbot.py is located at:
```config.ini
[PARAMETERS]
OPENAI_KEY = sk-xxxxxxxxxxxxxxxxxxxxxxx
SOURCE_DIR = ./functionalities/resources/texts
DATABASE_REFRESH_RATE = 60
```

- **OPENAI_KEY**: Your OpenAI API key. Be careful not to share it with anyone.
- **SOURCE_DIR**: The directory that contains your input documents.
- **DATABASE_REFRESH_RATE**: time in seconds. How often will the agent scan the directory
to see if there have been changes (i.e. document addition, deletion or modification).

### 3. Start the app

Go to the directory summarizerbot.py and the config.ini file are located at and run:
```bash
python summarizerbot.py
```

This command will get the app running: it loads and vectorizes the documents from your 
source directory, it launches the Gradio UI (and the underlying API) and, finally, it starts
the file change tracking so the changes you make to the files are reflected in the app in real time.


## 🧠 Functional Overview


### 🔍 Semantic File Search
Say what kind of content you are looking for and the system will suggest the files that best match your query and explain why.

### 📝 Extractive Summarization
Extract the most relevant sentences from a document. Short: 15% of the sentences in the text. Medium: 25%. Long: 40%. All percentages are rounded down (e.g. 10 sentence text, short summary, 0.15 * 10 = 1.5 -> 1 sentence long summary .
### 💫 Abstractive Summarization
Summarize a document by filename. If the filename is not found, the agent will attempt to match the documents whose meaning best match your query
### 💬 Chat with Documents
Conversational interface powered by LangChain's memory and retrieval chain. Have a chat about your documents.

## 📃 License

Creative Commons Attribution 4.0 International

You are free to:

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, including commercially.

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
  You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Full license text: https://creativecommons.org/licenses/by/4.0/

Author: Javier de Torres

## Author

Created by Javier de Torres, you can reach out to me on [LinkedIn](https://www.linkedin.com/in/javier-de-torres-a79668109/)

Thank you for using this app and have a nice day :).
