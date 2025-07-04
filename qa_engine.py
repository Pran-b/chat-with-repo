import os
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document


def load_code_files(repo_path):
    supported_exts = [".py", ".js", ".ts", ".md", ".txt", ".java", ".go"]
    docs = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in supported_exts):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        docs.append(Document(page_content=content, metadata={"source": filepath}))
                except Exception:
                    pass  # skip unreadable files
    return docs


def get_vectorstore(repo_path):
    docs = load_code_files(repo_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def get_qa_chain(vectorstore, model_name):
    llm = Ollama(model=model_name.replace("ollama:", ""))
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    return chain
