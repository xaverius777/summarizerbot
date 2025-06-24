import configparser
import os

# Get the configuration variables, as we need them to make some imports
config = configparser.ConfigParser()
config.read("config.ini")
api_key = config["PARAMETERS"]["OPENAI_KEY"]
source_dir = os.path.abspath(config["PARAMETERS"]["SOURCE_DIR"])
refresh_rate = int(config["PARAMETERS"].get("DATABASE_REFRESH_RATE", 60))
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_KEY"] = api_key
os.environ["SOURCE_DIR"] = source_dir

import threading
import gradio
from modules.vector_db_watcher import get_file_state, detect_changes
from modules.vector_db import load_vector_store, load_single_file, \
    get_documents_from_source_dir, get_chunks_from_docs, initialize_vector_db, add_chunks_to_vector_db
from time import sleep
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_runtime_file_watch_loop(source_dir, refresh_rate):
    previous_state = get_file_state(source_dir)
    while True:
        sleep(refresh_rate)
        current_state = get_file_state(source_dir)
        added, removed, modified = detect_changes(previous_state, current_state)

        if added or removed or modified:
            logger.info(f"Changes detected: added={added}, removed={removed}, modified={modified}")
            store = load_vector_store()
            # Remove old vectors
            for filename in removed + modified:
                store._collection.delete(where={"filename": filename})

            # Add new vectors
            to_add_files = added + modified
            for filename in to_add_files:
                filepath = os.path.join(source_dir, filename)
                docs = load_single_file(filepath)
                chunks = get_chunks_from_docs(docs)

                # store.add_documents(docs)
                add_chunks_to_vector_db(chunks)

            previous_state = current_state
        else:
            logger.debug("No changes detected.")


def main():
    docs = get_documents_from_source_dir(source_dir)
    chunks = get_chunks_from_docs(docs)
    initialize_vector_db(chunks)

    watcher_thread = threading.Thread(
        target=start_runtime_file_watch_loop,
        args=(source_dir, refresh_rate),
        daemon=True
    )
    watcher_thread.start()

    from modules.ai_assistant_chat import chat_tab
    from modules.abstractive_summarization import abstractive_tab
    from modules.extractive_summarization import extractive_tab
    from modules.semantic_file_search import search_tab
    gradio.TabbedInterface(
        [chat_tab,
         abstractive_tab,
         extractive_tab,
         search_tab
         ],
        tab_names=[
            "AI Assistant Chat",
            "Summarize (abstractive)",
            "Summarize (extractive)",
            "Find files by content"
        ]
    ).launch()


if __name__ == "__main__":
    main()
