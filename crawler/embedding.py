
import json
import time
from pathlib import Path

import ollama


# --------------------------------
# 1. PROJECT SETTINGS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "chunks.json"

# Separate output file: Gemini data remains untouched.
OUTPUT_FILE = (
    BASE_DIR / "data" / "processed" / "ollama_embeddings.json"
)

MODEL_NAME = "nomic-embed-text"

BATCH_SIZE = 16

EXPECTED_DIMENSIONS = 768


# --------------------------------
# 2. SAVE PROGRESS
# --------------------------------

def save_embeddings(embeddings):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Temporary file protects against incomplete writes.
    temp_file = OUTPUT_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(embeddings, file, ensure_ascii=False)

    temp_file.replace(OUTPUT_FILE)


# --------------------------------
# 3. LOAD EXISTING DATA
# --------------------------------

def load_data():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not isinstance(chunks, list):
        raise ValueError("Expected chunks.json to contain a list.")

    return chunks


def load_existing_embeddings():

    if not OUTPUT_FILE.exists():
        return []

    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------
# 4. GENERATE EMBEDDINGS
# --------------------------------

def create_embeddings():

    print("\nLoading website chunks...")

    chunks = load_data()

    existing_embeddings = load_existing_embeddings()

    completed_ids = {
        item["chunk_id"]
        for item in existing_embeddings
    }

    remaining_chunks = [
        chunk for chunk in chunks
        if chunk["chunk_id"] not in completed_ids
    ]

    print(f"Total website chunks: {len(chunks)}")
    print(f"Already embedded: {len(existing_embeddings)}")
    print(f"Remaining chunks: {len(remaining_chunks)}")

    if not remaining_chunks:
        print("\nAll embeddings are already generated!")
        return

    # --------------------------------
    # 5. PROCESS IN BATCHES
    # --------------------------------

    total_batches = (
        len(remaining_chunks) + BATCH_SIZE - 1
    ) // BATCH_SIZE

    for start in range(0, len(remaining_chunks), BATCH_SIZE):

        batch = remaining_chunks[
            start:start + BATCH_SIZE
        ]

        batch_number = start // BATCH_SIZE + 1

        texts = [
            chunk["content"]
            for chunk in batch
        ]

        print(
            f"\nProcessing batch {batch_number}/{total_batches}..."
        )

        try:

            response = ollama.embed(
                model=MODEL_NAME,
                input=texts
            )

            vectors = response["embeddings"]

            if len(vectors) != len(batch):
                raise ValueError(
                    "Number of returned vectors does not match batch size."
                )

            for chunk, vector in zip(batch, vectors):

                if len(vector) != EXPECTED_DIMENSIONS:
                    raise ValueError(
                        f"Unexpected vector dimensions: {len(vector)}"
                    )

                record = {
                    **chunk,
                    "embedding": vector
                }

                existing_embeddings.append(record)

            # Save after every successful batch.
            save_embeddings(existing_embeddings)

            print(
                f"Batch {batch_number} completed successfully."
            )

            print(
                f"Total saved: {len(existing_embeddings)}/{len(chunks)}"
            )

            time.sleep(0.2)

        except Exception as error:

            print("\nERROR:", error)
            print("Progress has been saved.")
            print("You can run the script again to resume.")

            return

    print("\n================================")
    print("OLLAMA EMBEDDINGS COMPLETED!")
    print("================================")

    print(f"Total embeddings: {len(existing_embeddings)}")
    print(f"Vector dimensions: {EXPECTED_DIMENSIONS}")
    print(f"Saved file: {OUTPUT_FILE}")


# --------------------------------
# 6. START PROGRAM
# --------------------------------

if __name__ == "__main__":

    create_embeddings()
