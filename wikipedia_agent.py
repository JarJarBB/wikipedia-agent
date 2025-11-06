import json
import os
from datetime import datetime
from langchain_community.retrievers import WikipediaRetriever
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize models and retriever
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
retriever = WikipediaRetriever(
    load_all_available_meta=True, top_k_results=1, doc_content_chars_max=1_000_000
)

# Log file path
LOG_FILE = "logs.json"


def log_interaction(user_question: str, summary: str) -> None:
    """Append a log entry to logs.json."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": user_question,
        "summary": summary
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def check_content(question: str) -> str:
    """Ask the LLM whether clarification is needed."""
    clarification_prompt = ChatPromptTemplate.from_template(
        """
        Check if this question is about one of these topics:
        * Computer Science
        * Engineering
        * Physics
        If so, respond with "APPROPRIATE_CONTENT".
        Otherwise, respond with "INAPPROPRIATE_CONTENT".
        The user asked: "{question}"
        """
    )

    chain = clarification_prompt | llm
    return chain.invoke(question).content.strip()


def ask_for_clarification(question: str) -> str:
    """Ask the LLM whether clarification is needed."""
    clarification_prompt = ChatPromptTemplate.from_template(
        """
        You are an AI assistant preparing to retrieve information from Wikipedia.
        The user asked: "{question}".
        If the question is ambiguous or incomplete, respond with a clarifying question.
        Otherwise, respond with "NO_CLARIFICATION_NEEDED".
        """
    )

    chain = clarification_prompt | llm
    return chain.invoke(question).content.strip()


def summarize_interaction(question: str, answer: str) -> str:
    """Summarize the interaction for logging."""
    summary_prompt = ChatPromptTemplate.from_template(
        """
        Summarize the interaction in one or two sentences:
        Question: {question}
        Answer: {answer}
        """
    )
    chain = summary_prompt | llm
    r = chain.invoke({"question": question, "answer": answer[:10000]})
    return r.content.strip()


def retrieve_from_wikipedia(query: str) -> str:
    """Retrieve quotes directly from Wikipedia."""
    docs = retriever.invoke(query)
    if not docs:
        return "No Wikipedia results found."

    quotes = []
    for d in docs:
        snippet = d.page_content.strip()
        title = d.metadata.get("title", "Unknown Title")
        quotes.append(f'From "{title}": "{snippet}"')
    return "\n\n".join(quotes)


def ai_agent() -> None:
    """Main loop for the AI agent."""
    print("🧠 Wikipedia Quote Agent (type 'exit' to quit)\n")
    while True:
        user_question = input("You: ").strip()
        if user_question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        check = check_content(user_question)
        if check != "APPROPRIATE_CONTENT":
            print("Agent: Let's not go there...\n")
            continue  # or handle as needed

        clarification = ask_for_clarification(user_question)
        if clarification != "NO_CLARIFICATION_NEEDED":
            print(f"Agent: {clarification}")
            user_question = input("You (clarified): ").strip()

        print("🔍 Searching Wikipedia...\n")
        final_answer = retrieve_from_wikipedia(user_question)

        print("\n📘 Content from Wikipedia:\n")
        print(final_answer)
        print("\n")

        # Summarize and log
        summary = summarize_interaction(user_question, final_answer)
        log_interaction(user_question, summary)
        print("📝 Interaction logged.\n")


if __name__ == "__main__":
    ai_agent()
