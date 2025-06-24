import gradio
from collections import defaultdict
from modules.vector_db import load_vector_store


def search_files_by_question(query: str, top_k_files=3, top_k_chunks_per_file=3) -> str:
    # Find top 30 chunks semantically relevant
    vector_store = load_vector_store()
    results = vector_store.similarity_search_with_score(query, k=30)
    # Group chunks by filename
    file_scores = defaultdict(list)
    for doc, score in results:
        filename = doc.metadata.get("filename", "unknown")
        file_scores[filename].append((score, doc.page_content))
    # Sort files by best chunk match
    ranked_files = sorted(file_scores.items(), key=lambda item: min(s for s, _ in item[1]))[:top_k_files]
    # Generate output with justification
    output = []
    for filename, chunks in ranked_files:
        top_chunks = sorted(chunks, key=lambda x: x[0])[:top_k_chunks_per_file]
        top_texts = "\n".join(f"- {text[:200]}..." for _, text in top_chunks)
        output.append(f"📄 **{filename}** might be relevant because:\n{top_texts}")
    return "\n\n".join(output)


search_tab = gradio.Interface(
    fn=search_files_by_question,
    inputs=gradio.Textbox(label="What are you looking for? (e.g., internet packets)"),
    outputs="markdown",
    title="📂 Semantic file search",
    description="Say what kind of content you are looking for and the system will suggest "
                " the files that best match your query and explain why."
)
