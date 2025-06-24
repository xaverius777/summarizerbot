import gradio
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from modules.vector_db import load_vector_store, SOURCE_DIR, MODEL


llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
# We can't update the embeddings live like other modules because, necessarily, we must use
# the same embeddings throughout the entire conversation
vector_store = load_vector_store()
retriever = vector_store.as_retriever()
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)


def chat(message, history):
    langchain_history = []
    for user_msg, ai_msg in history:
        langchain_history.append({"role": "user", "content": user_msg})
        langchain_history.append({"role": "assistant", "content": ai_msg})

    result = conversation_chain.invoke({
        "question": message,
        "chat_history": langchain_history
    })
    return result["answer"]


chat_tab = gradio.ChatInterface(
    fn=chat,
    title="💬 Chat with your documents",
    description=f"Ask anything about your document collection at {SOURCE_DIR}. The system will retrieve relevant"
                f" knowledge and reply in natural language.",
    theme="soft",
    examples=[
        "How do satellites work?",
        "What do astrophysicists study?",
    ],
    autoscroll=True,
    editable=True
)