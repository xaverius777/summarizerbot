import glob
from langchain_community.document_loaders import TextLoader as LCTextLoader, PyMuPDFLoader,\
    UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import logging
import os
from langchain_chroma import Chroma


class UTF8TextLoader(LCTextLoader):
    def __init__(self, file_path):
        super().__init__(file_path, encoding="utf-8")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MODEL = "gpt-4o-mini"
DB_NAME = "vector_db"
SOURCE_DIR = os.environ.get("SOURCE_DIR")
EMBEDDINGS = OpenAIEmbeddings()


def get_documents_from_source_dir(source_directory):
    docs = []
    for filepath in glob.glob(os.path.join(source_directory, "*")):
        extension = os.path.splitext(filepath)[1].lower()
        if extension == ".txt":
            loader = UTF8TextLoader(filepath)
        elif extension == ".pdf":
            loader = PyMuPDFLoader(filepath)
        elif extension == ".docx":
            loader = UnstructuredWordDocumentLoader(filepath)
        else:
            logger.warning(
                f"Extension {extension} not supported, so will skip document {filepath}. Supported extensions: "
                f" .txt, .docx, .pdf.")
            continue
        # logger.info(f"Successfully loaded file {filepath}")
        single_doc_list = loader.load()
        # print(len(file_docs), file_docs)
        for doc in single_doc_list:
            doc.metadata["filename"] = os.path.basename(filepath)
            doc.metadata["topic"] = os.path.basename(filepath).split("_")[0]
        docs.extend(single_doc_list)
    return docs


def load_single_file(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    if extension == ".txt":
        loader = UTF8TextLoader(filepath)
    elif extension == ".pdf":
        loader = PyMuPDFLoader(filepath)
    elif extension == ".docx":
        loader = UnstructuredWordDocumentLoader(filepath)
    else:
        logger.warning(f"Unsupported extension {extension} in file {filepath}")
        return []

    single_doc_list = loader.load()
    for doc in single_doc_list:
        doc.metadata["filename"] = os.path.basename(filepath)
        doc.metadata["topic"] = os.path.basename(filepath).split("_")[0]
    return single_doc_list


def get_chunks_from_docs(docs):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    return chunks


def initialize_vector_db(chunks):
    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME, embedding_function=EMBEDDINGS).delete_collection()
    vector_store = Chroma.from_documents(documents=chunks, embedding=EMBEDDINGS, persist_directory=DB_NAME)
    # vector_store.persist()
    logger.info("Successfully transformed the documents in the source directory to vectors"
                " and stored them in a vector database")
    return vector_store


def load_vector_store():
    return Chroma(persist_directory=DB_NAME, embedding_function=EMBEDDINGS)


def add_chunks_to_vector_db(chunks):
    store = load_vector_store()
    if chunks:
        store.add_documents(chunks)
