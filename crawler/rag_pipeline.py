from crawler.retriever import search_website
from crawler.generator import generate_answer


def ask_question(question):

    print("\nSearching website knowledge...")

    # STEP 1: Retrieve relevant website chunks
    results = search_website(question, top_k=5)

    # STEP 2: Prepare context from retrieved chunks
    context_parts = []

    for result in results:

        title = result["metadata"]["title"]
        url = result["metadata"]["url"]
        content = result["content"]

        context_parts.append(
            f"""
Website Page: {title}
URL: {url}

Content:
{content}
"""
        )

    context = "\n\n".join(context_parts)

    # STEP 3: Generate answer using Qwen
    print("\nGenerating answer using LLM...")

    answer = generate_answer(
        question=question,
        context=context
    )

    return answer


# --------------------------------
# TEST COMPLETE RAG PIPELINE
# --------------------------------

if __name__ == "__main__":

    print("================================")
    print("SKILL LEARNING ACADEMY AI CHATBOT")
    print("================================")

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break

        answer = ask_question(question)

        print("\nChatbot:", answer)
