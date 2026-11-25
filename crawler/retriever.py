
import chromadb
import ollama
from pathlib import Path


# --------------------------------
# 1. CONFIGURATION
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

COLLECTION_NAME = "skill_learning_website"

MODEL_NAME = "nomic-embed-text"


# --------------------------------
# 2. CONNECT TO CHROMADB
# --------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# --------------------------------
# 3. SEARCH FUNCTION
# --------------------------------

def search_website(question, top_k=5):

    print("\nGenerating question embedding...")

    response = ollama.embed(
        model=MODEL_NAME,
        input=question
    )

    query_embedding = response["embeddings"][0]

    print("Searching website knowledge...")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    for i in range(len(results["ids"][0])):

        chunk = {
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        }

        retrieved_chunks.append(chunk)

    return retrieved_chunks


# --------------------------------
# 4. TEST RETRIEVER
# --------------------------------

if __name__ == "__main__":

    question = input("\nAsk something about Skill Learning Academy: ")

    results = search_website(question)

    print("\n========== SEARCH RESULTS ==========")

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Title:", result["metadata"]["title"])
        print("URL:", result["metadata"]["url"])
        print("Distance:", result["distance"])
        print("Content:")
        print(result["content"][:500])
        print("-" * 60)
