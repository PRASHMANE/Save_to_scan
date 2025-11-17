# streamlit_rag_chatbot.py

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import re
import os
from dotenv import load_dotenv

# -----------------------------
# Load API key
# -----------------------------
load_dotenv()
api_key = os.getenv("API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

# -----------------------------
# Helper function to clean Markdown bullets
# -----------------------------
def clean_asterisks(text: str) -> str:
    cleaned_text = text.replace("*", "")
    cleaned_text = re.sub(r"^\s+", "", cleaned_text, flags=re.MULTILINE)
    return cleaned_text

# -----------------------------
# Streamlit app UI
# -----------------------------
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("📄 RAG Chatbot - Ask Questions about your PDF")
st.markdown("Type your question below and click the arrow to get the answer.")

# Input box with arrow button
user_input = st.text_input("Ask your question here:", placeholder="Type your question...")

if st.button("➡️ Get Answer"):
    if not user_input.strip():
        st.warning("Please type a question!")
    else:
        with st.spinner("Fetching answer... ⏳"):

            # -----------------------------
            # Initialize LLM
            # -----------------------------
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                temperature=0,
                api_key=api_key
            )

            # -----------------------------
            # Load PDF and create chunks
            # -----------------------------
            loader = PyPDFLoader("/Users/prashmane/Documents/Almabetter/a.pdf")
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100
            )
            chunks = text_splitter.split_documents(documents)

            # -----------------------------
            # Create embeddings and vectorstore
            # -----------------------------
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            db = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name="rag_pdf",
                persist_directory="./chroma_store"
            )
            retriever = db.as_retriever()

            # -----------------------------
            # Prompt template
            # -----------------------------
            prompt = ChatPromptTemplate.from_template("""
Use the following context to answer the question in step by step with short explanation who to save the person .

Context:
{context}

Question:
{question}

Answer:
""")

            # -----------------------------
            # Build RAG chain
            # -----------------------------
            rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            # -----------------------------
            # Invoke chain and clean output
            # -----------------------------
            ans = rag_chain.invoke(user_input)
            ans = clean_asterisks(ans)

            # -----------------------------
            # Display answer
            # -----------------------------
            st.markdown("**Answer:**")
            st.text(ans)
