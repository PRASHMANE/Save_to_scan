from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from IPython.display import display, Markdown
import re


def clean_asterisks(text: str) -> str:
    """
    Remove Markdown bullets (*) and extra spaces from text.
    """
    # Remove all asterisks used for Markdown bold/italics
    cleaned_text = text.replace("*", "")
    
    # Remove extra spaces at line beginnings
    cleaned_text = re.sub(r"^\s+", "", cleaned_text, flags=re.MULTILINE)
    
    return cleaned_text


from dotenv import load_dotenv

import os
load_dotenv()

api_key=os.getenv("API_KEY")

os.environ["GOOGLE_API_KEY"] = api_key

from langchain_google_genai import GoogleGenerativeAIEmbeddings






llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro", 
    temperature=0,
    api_key=api_key
)

loader = PyPDFLoader("/Users/prashmane/Documents/Almabetter/a.pdf")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="rag_pdf",
    persist_directory="./chroma_store"
)

retriever = db.as_retriever()


prompt = ChatPromptTemplate.from_template("""
Use the following context to answer the question. in step by step with short explanation

Context:
{context}

Question:
{question}

Answer:
""")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

ans=rag_chain.invoke("ABCs of first aid")
ans=clean_asterisks(ans)
print(ans)