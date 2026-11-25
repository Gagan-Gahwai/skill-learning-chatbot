# 🤖 AI Website Knowledge Chatbot – RAG Based

An intelligent, standalone website chatbot that answers user questions using information extracted from a website. It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant website content and generate contextual answers using a locally running Large Language Model (LLM).

This project currently uses [Skill Learning Academy](https://www.skilllearningacademy.com/) as its knowledge source.

The chatbot is built using Python, Streamlit, Ollama, and ChromaDB.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Project Objectives](#-project-objectives)
4. [Key Features](#-key-features)
5. [Technology Stack](#-technology-stack)
6. [System Architecture](#-system-architecture)
7. [How RAG Works](#-how-rag-works)
8. [Project Structure](#-project-structure)
9. [Installation and Setup](#-installation-and-setup)
10. [Running the Project](#-running-the-project)
11. [Project Workflow](#-project-workflow)
12. [Models Used](#-models-used)
13. [Advantages](#-advantages)
14. [Limitations](#-limitations)
15. [Future Improvements](#-future-improvements)
16. [Learning Outcomes](#-learning-outcomes)
17. [Disclaimer](#-disclaimer)
18. [Author](#-author)

---

## 🚀 Project Overview

The AI Website Knowledge Chatbot is a Retrieval-Augmented Generation (RAG) application designed to understand and answer questions about website content.

Traditional website visitors often need to navigate multiple pages to find specific information about courses, programs, training, and other services.

This chatbot simplifies that experience.

Instead of manually searching through website pages, users can ask questions in natural language and receive relevant answers generated using the information retrieved from the website.

The application follows a RAG architecture:

- **Retrieval:** Finds relevant information from the website knowledge base.
- **Augmentation:** Provides the retrieved information as context to the LLM.
- **Generation:** Generates a natural-language answer based on that context.

The application runs locally using Ollama for embeddings and language generation.

## 🎯 Problem Statement

Many websites contain large amounts of information distributed across multiple pages.

Visitors may experience difficulties when:

- Finding specific course information.
- Understanding available training programs.
- Searching for information across multiple pages.
- Getting quick answers to their questions.

This project aims to solve this problem by providing an AI-powered conversational interface that retrieves relevant website information and generates contextual responses.

## 🎯 Project Objectives

- Automatically discover website pages.
- Extract meaningful content from website pages.
- Clean and preprocess extracted information.
- Divide website content into smaller text chunks.
- Generate vector embeddings for semantic search.
- Store embeddings in a vector database.
- Retrieve relevant information based on user questions.
- Generate contextual answers using an LLM.
- Provide an interactive chatbot interface.

---

## ✨ Key Features

### 1. Website Crawling
Automatically discovers website URLs and collects website content.

### 2. Dynamic Website Scraping
Uses Playwright to extract content from JavaScript-rendered website pages.

### 3. Text Preprocessing
Cleans extracted website content and removes unnecessary information.

### 4. Text Chunking
Splits large website content into smaller chunks with overlapping text to preserve context.

### 5. Local Embeddings
Uses the `nomic-embed-text` model through Ollama to convert text into numerical vector representations.

### 6. Vector Database
Uses ChromaDB to store and search vector embeddings.

### 7. Semantic Search
Retrieves relevant website content based on the meaning of a user's question rather than only matching keywords.

### 8. AI-Powered Answer Generation
Uses the `qwen2.5:1.5b-instruct` model through Ollama to generate natural-language answers.

### 9. Interactive Chatbot
Provides a conversational interface using Streamlit.

### 10. Local LLM Execution
Runs the embedding and generation models locally through Ollama, avoiding dependence on paid LLM inference APIs for the main RAG workflow.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Chatbot frontend |
| Playwright | Dynamic website scraping |
| BeautifulSoup | HTML parsing |
| Requests | HTTP requests |
| Ollama | Local model execution |
| nomic-embed-text | Text embeddings |
| Qwen 2.5 1.5B Instruct | Answer generation |
| ChromaDB | Vector database |
| JSON | Intermediate data storage |
| Git & GitHub | Version control |

---

## 🏗️ System Architecture

The application follows a Retrieval-Augmented Generation architecture.

```text
             WEBSITE
                |
                v
        Website Discovery
                |
                v
         Website Scraping
                |
                v
        Text Preprocessing
                |
                v
          Text Chunking
                |
                v
       Embedding Generation
          (Ollama)
                |
                v
          ChromaDB
        Vector Database
                |
                |
       USER ASKS QUESTION
                |
                v
        Streamlit Interface
                |
                v
       Question Embedding
          (Ollama)
                |
                v
       Semantic Retrieval
          (ChromaDB)
                |
                v
       Relevant Text Chunks
                |
                v
       Context + User Query
                |
                v
         Qwen LLM
                |
                v
        Generated Answer
                |
                v
          CHATBOT UI
```

---

## 🧠 How RAG Works

RAG stands for **Retrieval-Augmented Generation**.

It combines information retrieval with Large Language Models.

Instead of asking an LLM to answer everything using only its pre-trained knowledge, RAG provides relevant information from an external knowledge source.

### Step 1: Website Discovery

The application discovers available website URLs using website sitemap information and URL discovery techniques.

### Step 2: Website Scraping

Playwright loads website pages and extracts rendered HTML content.

BeautifulSoup processes the HTML to extract meaningful text.

### Step 3: Text Preprocessing

The extracted content is cleaned by removing unnecessary elements and formatting.

### Step 4: Text Chunking

Large documents are divided into smaller chunks.

Current configuration:

- Chunk size: 1,000 characters.
- Chunk overlap: 150 characters.
- Total processed chunks: 766.

Overlapping helps preserve contextual continuity between neighboring chunks.

### Step 5: Embedding Generation

The `nomic-embed-text` model converts each text chunk into a numerical vector.

These vectors represent the semantic meaning of the text.

### Step 6: Vector Storage

ChromaDB stores the embeddings along with their corresponding text and metadata.

### Step 7: User Query

The user enters a question through the Streamlit chatbot interface.

### Step 8: Query Embedding

The same embedding model converts the user's question into a vector.

### Step 9: Semantic Retrieval

ChromaDB searches for the most relevant stored vectors using similarity search.

The application retrieves the top five relevant chunks.

### Step 10: Answer Generation

The retrieved information is passed to the Qwen language model as context.

The model generates a response based on the supplied context.

### Step 11: Display Answer

The generated response is displayed to the user through the Streamlit interface.

---

## 📁 Project Structure

```text
ai-website-rag-chatbot/
│
├── crawler/
│   ├── discover.py
│   ├── scraper.py
│   ├── preprocess.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│   └── rag_pipeline.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── vector_store/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Folder Description

| File / Folder | Responsibility |
|---|---|
| `crawler/discover.py` | Discovers website URLs |
| `crawler/scraper.py` | Extracts website content |
| `crawler/preprocess.py` | Cleans and chunks text |
| `crawler/embedding.py` | Handles embedding generation |
| `crawler/vector_store.py` | Stores embeddings in ChromaDB |
| `crawler/retriever.py` | Retrieves relevant content |
| `crawler/generator.py` | Generates answers using the LLM |
| `crawler/rag_pipeline.py` | Connects retrieval and generation |
| `frontend/app.py` | Streamlit chatbot interface |
| `main.py` | FastAPI prototype |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes unnecessary and sensitive files |

*Note: The `data/` and local vector database folders are generated during processing and are not included in the GitHub repository.*

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Make sure you have installed:

- Python 3.10 or higher.
- Git.
- Ollama.
- A supported Ollama model.
- VS Code or another code editor.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-website-rag-chatbot.git
```

Navigate into the project directory:

```bash
cd ai-website-rag-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Download Ollama:

https://ollama.com/

Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

Pull the language model:

```bash
ollama pull qwen2.5:1.5b-instruct
```

Verify the installed models:

```bash
ollama list
```

Make sure Ollama is running before starting the application.

### 5. Prepare Website Data

The project requires the website's content, embeddings, and ChromaDB collection to be generated before chatbot queries can work.

The data-generation workflow is:

1. Discover website URLs.
2. Scrape website content.
3. Preprocess and chunk the content.
4. Generate embeddings.
5. Create and populate the ChromaDB collection.

The generated files are stored locally and excluded from GitHub.

Use the scripts in the `crawler/` directory to execute these stages. The current knowledge base is based on Skill Learning Academy.

---

## ▶️ Running the Project

After installing dependencies, configuring Ollama, and preparing the vector database, start the Streamlit application:

```bash
python -m streamlit run frontend/app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

You can now start interacting with the chatbot.

---

## 💬 Example Questions

Try asking questions such as:

- What courses does Skill Learning Academy offer?
- Which courses teach Python programming?
- What training programs are available?
- Tell me about the academy's AI-related courses.
- What are the available learning programs?

The chatbot retrieves relevant information from its website knowledge base and generates answers using the LLM.

---

## 🌟 Advantages

- Provides a conversational way to explore website information.
- Uses semantic search instead of simple keyword matching.
- Reduces the need to manually navigate multiple pages.
- Uses local LLMs through Ollama.
- Keeps the website knowledge base separate from the language model.
- Can be extended to support other website knowledge sources.
- Demonstrates practical implementation of a complete RAG pipeline.

---

## ⚠️ Limitations

- The current knowledge base is built around one website.
- Answers depend on the quality and freshness of the scraped content.
- The website must be scraped again when its content changes.
- Local LLM performance depends on available system resources.
- Some dynamically rendered or inaccessible pages may not be collected.
- The current application does not guarantee that every generated answer is factually correct.
- A prepared local vector database is required before asking questions.

---

## 🔮 Future Improvements

Planned improvements include:

- [ ] Allow users to enter any public website URL.
- [ ] Automatically crawl and index new websites.
- [ ] Add source links to generated answers.
- [ ] Improve retrieval accuracy and relevance.
- [ ] Add conversation history and persistent chat sessions.
- [ ] Add document upload support for PDF and DOCX.
- [ ] Add support for multiple embedding models.
- [ ] Add configurable LLM providers such as Groq and Gemini.
- [ ] Add a more advanced and responsive chatbot interface.
- [ ] Add deployment support.
- [ ] Add evaluation metrics for retrieval and answer quality.

---

## 📚 Learning Outcomes

While building this project, I explored and implemented several practical concepts:

- Web scraping and dynamic website rendering.
- HTML parsing and text preprocessing.
- Text chunking and chunk overlap.
- Vector embeddings and semantic representations.
- Vector databases and ChromaDB.
- Semantic similarity search.
- Retrieval-Augmented Generation (RAG).
- Prompt engineering and context management.
- Local LLM integration using Ollama.
- Building AI applications using Streamlit.
- Python project organization and Git version control.

This project helped me understand how different components of a practical RAG application work together.

---

## ⚖️ Disclaimer

This is an independent educational and portfolio project.

It is not officially affiliated with or endorsed by Skill Learning Academy.

Website content is used as the knowledge source for demonstration purposes. Users should respect the website's terms of use, copyright, and applicable scraping policies.

The chatbot may generate inaccurate responses. Always verify important information with the original website.

---

## 👨‍💻 Author

**Gagan Gahwai**

AI Engineer Intern | Python | Machine Learning | Generative AI | RAG

- GitHub: https://github.com/YOUR_USERNAME
- LinkedIn: https://www.linkedin.com/in/YOUR_LINKEDIN_USERNAME/

If you find this project interesting, feel free to explore the repository and share your feedback.

⭐ If you like this project, consider giving it a star!
