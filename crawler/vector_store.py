
import json
from pathlib import Path

import chromadb


# --------------------------------
# 1. PROJECT PATHS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDINGS_FILE = (
    BASE_DIR / "data" / "processed" / "ollama_embeddings.json"
)

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"


# --------------------------------
# 2. LOAD EMBEDDINGS
# --------------------------------

def load_embeddings():

    print("Loading Ollama embeddings...")

    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"Total embeddings loaded: {len(data)}")

    return data


# --------------------------------
# 3. CREATE CHROMADB CLIENT
# --------------------------------

def create_database():

    print("\nConnecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    print("ChromaDB connected successfully!")

    return client


# --------------------------------
# 4. CREATE COLLECTION
# --------------------------------

def create_collection(client):

    collection = client.get_or_create_collection(
        name="skill_learning_website",
        metadata={"hnsw:space": "cosine"}
    )

    print("Collection ready!")

    return collection


# --------------------------------
# 5. INSERT EMBEDDINGS
# --------------------------------

def insert_embeddings(collection, data):

    print("\nInserting embeddings into ChromaDB...")

    batch_size = 100

    for start in range(0, len(data), batch_size):

        batch = data[start:start + batch_size]

        collection.upsert(
            ids=[
                item["chunk_id"]
                for item in batch
            ],

            embeddings=[
                item["embedding"]
                for item in batch
            ],

            documents=[
                item["content"]
                for item in batch
            ],

            metadatas=[
                {
                    "url": item["url"],
                    "title": item["title"],
                    "chunk_index": item["chunk_index"]
                }
                for item in batch
            ]
        )

        print(
            f"Inserted {min(start + batch_size, len(data))}/{len(data)}"
        )

    print("\nAll embeddings inserted successfully!")


# --------------------------------
# 6. VERIFY DATABASE
# --------------------------------

def verify_database(collection):

    print("\nVerifying ChromaDB...")

    total = collection.count()

    print(f"Total records in database: {total}")

    if total == 766:
        print("SUCCESS: All website chunks are stored!")
    else:
        print("WARNING: Record count does not match 766.")


# --------------------------------
# 7. MAIN FUNCTION
# --------------------------------

def main():

    data = load_embeddings()

    client = create_database()

    collection = create_collection(client)

    insert_embeddings(collection, data)

    verify_database(collection)


if __name__ == "__main__":
    main()
