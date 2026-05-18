from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import glob

GROQ_API_KEY = "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"

# Verileri yükle
documents = []
for filepath in glob.glob("data/*.txt"):
    loader = TextLoader(filepath, encoding="utf-8")
    documents.extend(loader.load())

# Chunk'lara böl
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Embedding ve vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db")
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# LLM
llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

def ask(question):
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    
    prompt = f"""Aşağıdaki platform kurallarına dayanarak soruyu Türkçe yanıtla.

Kurallar:
{context}

Soru: {question}

Yanıt:"""
    
    response = llm.invoke(prompt)
    return response.content