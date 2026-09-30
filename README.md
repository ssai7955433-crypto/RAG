# Local RAG Workshop

This project is a lightweight, beginner-friendly retrieval-augmented generation (RAG) application designed for a live classroom demonstration. It allows a user to upload a PDF or DOCX file, extract text, split it into chunks, generate embeddings locally, perform cosine-similarity retrieval, and pass the most relevant context to a local Ollama LLM.

## Workflow

Document
→ Extract
→ Clean
→ Chunk
→ Embed
→ Compare
→ Retrieve
→ Context
→ LLM
→ Answer

## What the app does

- Accepts PDF and DOCX uploads
- Extracts textual content locally
- Cleans and chunks text meaningfully
- Generates embeddings with SentenceTransformers
- Uses cosine similarity to find relevant chunks
- Selects an Ollama model by priority: Qwen, then Llama
- Shows retrieval results and context transparency
- Returns grounded answers based on uploaded documents

## Model policy

- Primary: Qwen family if installed locally
- Fallback: Llama family if Qwen is not installed
- If neither is installed, the UI shows clear instructions instead of crashing

## Setup

1. Create a virtual environment.
2. Install dependencies.
3. Install Ollama.
4. Pull a local model such as `qwen3` or `llama3.2`.
5. Run the Streamlit app.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Ollama setup

Install Ollama from https://ollama.com/download and verify:

```bash
ollama list
```

Then install a model:

```bash
ollama pull qwen3
```

If Qwen is not available:

```bash
ollama pull llama3.2
```

## Project structure

```text
rag_workshop/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── document_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── ollama_client.py
│   ├── model_selector.py
│   └── rag_pipeline.py
├── ui/
│   ├── components.py
│   └── styles.py
├── data/
│   └── uploads/
├── tests/
│   ├── test_chunking.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   └── test_model_selection.py
└── .streamlit/
```

## Educational explanation

RAG is not magic memory. It first retrieves relevant passages from the uploaded document, then gives those passages to a local language model as evidence. The model then answers using that context instead of inventing information.

## Troubleshooting

- If Ollama is unavailable, install and start the service.
- If no local model is detected, install `qwen3` or `llama3.2`.
- If a PDF fails to parse, confirm the file is not encrypted or image-only.
- If a DOCX fails to parse, check that it contains readable text.
- If retrieval returns nothing, ask a question closer to the uploaded document content.

## Example workshop prompts

- What are the eligibility requirements?
- Which sections mention grading policy?
- Summarize the key timeline in this document.
- What is the role of the instructor described here?

## Important teaching point

Embeddings represent semantic meaning as vectors. Cosine similarity compares the angle between vectors to measure how related two ideas are. In RAG, the system embeds the user question and each document chunk, then retrieves the chunk vectors that are most similar to the question.

## License

This project is intended for educational workshop use.
