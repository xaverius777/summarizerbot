import os
import gradio
from langchain_community.document_loaders import TextLoader as LCTextLoader, PyMuPDFLoader, \
    UnstructuredWordDocumentLoader
import nltk
import re
import heapq
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from modules.vector_db import SOURCE_DIR
import logging


class UTF8TextLoader(LCTextLoader):
    def __init__(self, file_path):
        super().__init__(file_path, encoding="utf-8")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nltk.download('punkt')
nltk.download('stopwords')


def clean_text(txt):
    text = re.sub(r"\[[0-9]*\]", " ", txt)
    text = text.lower()
    text = re.sub(r'\s+', " ", text)
    text = re.sub(r",", " ", text)
    return text


def extractive_summarize(filename, length):
    filepath = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(filepath):
        return f"File '{filename}' not found."
    extension = os.path.splitext(filename)[1].lower()
    if extension == ".txt":
        loader = UTF8TextLoader(filepath)
    elif extension == ".pdf":
        loader = PyMuPDFLoader(filepath)
    elif extension == ".docx":
        loader = UnstructuredWordDocumentLoader(filepath)
    else:
        raise Exception(f"Extension {extension} not supported, so will skip document {filepath}. Supported extensions: "
                        f" .txt, .docx, .pdf.")
    single_doc_list = loader.load()
    full_text = "\n\n".join([doc.page_content for doc in single_doc_list])
    cleaned_text = clean_text(full_text)
    # Word frequencies
    word_tokens = word_tokenize(cleaned_text)
    stop_words = set(stopwords.words("english"))
    words_frequency = {}
    for word in word_tokens:
        if word not in stop_words:
            if word not in words_frequency:
                words_frequency[word] = 1
            else:
                words_frequency[word] += 1
    if not words_frequency:
        return "Text has no valid content after cleaning."
    max_freq = max(words_frequency.values())
    for word in words_frequency:
        words_frequency[word] = words_frequency[word] / max_freq
    # Sentence scoring
    sentence_tokens = sent_tokenize(cleaned_text)
    sentence_scores = {}
    for sentence in sentence_tokens:
        if len(sentence.split(" ")) < 30:
            for word in word_tokenize(sentence):
                if word in words_frequency:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = words_frequency[word]
                    else:
                        sentence_scores[sentence] += words_frequency[word]
    # Decide N based on length
    total_sentences = len(sentence_tokens)
    if total_sentences == 0:
        return "No sentences to summarize."
    ratio = {"short": 0.15, "medium": 0.3, "long": 0.4}.get(length, 0.3)
    n = max(1, int(total_sentences * ratio))  # At least one sentence
    summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)
    return " ".join(summary_sentences)


extractive_tab = gradio.Interface(
    fn=extractive_summarize,
    inputs=[
        gradio.Textbox(label="Filename (e.g., satellites_2.txt)"),
        gradio.Dropdown(["short", "medium", "long"], label="Summary length", value="medium")
    ],
    outputs="text",
    title="🔍 Extractive summarization",
    description="Extract the most relevant sentences from a document. Short: 15% of the sentences in the text. "
                "Medium: 25%. Long: 40%. All percentages are rounded down (e.g. 10 sentence text, short summary, "
                "0.15 * 10 = 1.5 -> 1 sentence long summary ."
)
