# 🧠 Wikipedia AI Agent

This project is a LangChain-based **AI Agent** that:

- Takes user questions
- Checks if the query matches an allowlist of topics
- Asks clarifying questions if necessary
- Retrieves **exact quotes** from Wikipedia
- Logs each interaction (with a summary) into a `logs.json` file

---

## 🧩 Requirements

Ensure Python 3.9+ is installed, then run:

```bash
pip install langchain langchain-community langchain-openai wikipedia python-dotenv
```

You will also need an OpenAI API key. Create a `.env` file in the project root and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

---

## ⚙️ Usage

Run the script directly:

```bash
python3 wikipedia_agent.py
```

You’ll be prompted for questions. Type `exit` to quit.

Example interaction:

```
🧠 Wikipedia Quote Agent (type 'exit' to quit)

You: Tell me more about the second law of thermodynamics.
🔍 Searching Wikipedia...

📘 Exact Quote from Wikipedia:

From "Max Planck": "Max Karl Ernst Ludwig Planck (German: [maks ˈplaŋk] ; 23 April 1858 – 4 October 1947) was a German theoretical physicist whose..."
```

---

## 📝 Logging

All interactions are saved in a JSON file named `logs.json` in the same directory.  
Example log entry:

```json
{
  "timestamp": "2025-11-05T20:56:21.036487",
  "question": "Tell me more about the second law of thermodynamics.",
  "summary": "The interaction involved a request for information about the second law..."
}
```

---

## 🧠 Flow Overview

```
User Input → LLM Checks Content → LLM Clarification → WikipediaRetriever → Quote Extraction → Summary → Logging
```
