import gradio
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from modules.vector_db import load_vector_store, MODEL

llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
prompt = PromptTemplate.from_template("""
You are a helpful summarization assistant.
Summarize the following text in a {length} summary:
{text}
""")
summary_chain = LLMChain(llm=llm, prompt=prompt)


def get_relevant_chunks_by_topic(topic: str):
    vector_store = load_vector_store()
    return vector_store.similarity_search(query=topic, k=10, filter={"topic": topic})


def get_relevant_chunks_by_filename(filename: str):
    vector_store = load_vector_store()
    return vector_store.similarity_search(query=filename, k=10, filter={"filename": filename})


def summarize_chunks(chunks: list[Document], length="medium"):
    content = "\n\n".join([c.page_content for c in chunks])
    return summary_chain.invoke({"text": content, "length": length})["text"]


def summarize_interface(doc_type_or_file, summary_length):
    if doc_type_or_file.endswith((".txt", ".pdf", ".docx")):
        chunks = get_relevant_chunks_by_filename(doc_type_or_file)
    else:
        chunks = get_relevant_chunks_by_topic(doc_type_or_file)
    if not chunks:
        return "No content found."
    return summarize_chunks(chunks, summary_length)


abstractive_tab = gradio.Interface(
    fn=summarize_interface,
    inputs=[
        gradio.Textbox(label="Filename (e.g. astronomy_1.txt)"),
        gradio.Dropdown(["short", "medium", "long"], label="Summary length"),
    ],
    outputs="markdown",
    title="📝 Abstractive summarization",
    description="Summarize a document by filename. If the filename is not found, the agent will attempt to match the "
                " documents whose meaning best match your query"
)
