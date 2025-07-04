# 🐙 Chat with a Git Repo

Interact with your codebase using natural language! Upload a GitHub repository URL or a `.zip` file of your project and ask questions like:

- "What does this repo do?"
- "Summarize the logic in `main.py`"
- "Which files handle authentication?"

Powered entirely by local models using [Ollama](https://ollama.com/) and [LangChain](https://python.langchain.com/).

---

## 🚀 Features

- 🧠 Local LLMs via Ollama (Mistral, LLaMA2, Qwen, etc.)
- 🔎 Automatic repo indexing using sentence-transformer embeddings
- 📦 Upload public GitHub repos or private `.zip` archives
- 💬 Ask questions about your codebase
- 🧰 No API keys required (fully offline)

---

## 🛠️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure you have [Ollama installed](https://ollama.com/download) and running:

```bash
ollama run mistral
```

---

## 🧪 Usage

```bash
streamlit run app.py
```

Then in the UI:
1. Choose input method (GitHub URL or `.zip`)
2. Select or type an Ollama model
3. Ask any question about your repo!

---

## 📌 Example Questions

- "Explain how the data pipeline works."
- "What is the purpose of `config.yaml`?"
- "Where is the entrypoint for this app?"

---

## 🧩 Supported File Types

- `.py`, `.js`, `.ts`, `.md`, `.txt`, `.java`, `.go`

---

## 🤖 LLM Compatibility

Tested with:
- `mistral`
- `llama2`
- `qwen3:0.6b`
- `gemma`

Add your own via:
```bash
ollama pull <model_name>
```

---

## 📜 License

MIT License
