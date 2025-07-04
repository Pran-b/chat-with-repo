import streamlit as st
import tempfile
import subprocess
from git_utils import process_repo
from qa_engine import get_vectorstore, get_qa_chain

st.set_page_config(page_title="Chat with a Git Repo", page_icon="🐙")
st.title("🐙 Chat with a Git Repository")

input_mode = st.radio("Choose input method", ["GitHub URL", ".zip file"], horizontal=True)

repo_path = None

if input_mode == "GitHub URL":
    github_url = st.text_input("Enter GitHub repository URL", key="repo_url")
    if github_url:
        with st.spinner("Cloning repository..."):
            repo_path = process_repo(repo_url=github_url)

elif input_mode == ".zip file":
    zip_file = st.file_uploader("Upload .zip file of repository", type="zip", key="zip_repo")
    if zip_file:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = f"{tmpdir}/uploaded.zip"
            with open(zip_path, "wb") as f:
                f.write(zip_file.read())
            repo_path = process_repo(zip_path=zip_path)

if repo_path:
    st.success("✅ Repository loaded successfully!")

    # Auto-detect available Ollama models
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()[1:]  # skip header
        model_names = [line.split()[0] for line in lines if line.strip()]
    except Exception as e:
        model_names = ["mistral", "llama2", "gemma"]
        st.warning(f"⚠️ Could not auto-detect Ollama models: {e}")

    model_names.append("other")
    model = st.selectbox("Choose Ollama model", model_names, key="ollama_model")
    if model == "other":
        model = st.text_input("Enter custom model name", key="ollama_custom")

    with st.spinner("Indexing codebase..."):
        vectorstore = get_vectorstore(repo_path)
        qa_chain = get_qa_chain(vectorstore, f"ollama:{model}")

    question = st.text_input("Ask a question about this repo")
    if question:
        with st.spinner("Thinking..."):
            response = qa_chain.run(question)
            st.write(response)

else:
    st.info("👆 Upload a repo to begin chatting!")
