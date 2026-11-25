
import json
import re

from pathlib import Path


# ======================================
# 1. CONFIGURATION
# ======================================

INPUT_FILE = Path("data/raw/website_content.json")

OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ======================================
# 2. CLEAN TEXT
# ======================================

def clean_text(text):
    """
    Remove unnecessary whitespace and clean text.
    """

    # Replace multiple spaces with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text


# ======================================
# 3. SPLIT TEXT INTO CHUNKS
# ======================================

def split_into_chunks(text):
    """
    Split text into overlapping chunks.
    """

    chunks = []

    # Split using paragraphs first
    paragraphs = text.split("\n")

    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Handle paragraphs larger than chunk size
        if len(paragraph) > CHUNK_SIZE:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            start = 0

            while start < len(paragraph):

                end = start + CHUNK_SIZE

                chunks.append(paragraph[start:end])

                start += CHUNK_SIZE - CHUNK_OVERLAP

            continue

        # Check whether paragraph fits
        if len(current_chunk) + len(paragraph) + 1 <= CHUNK_SIZE:

            if current_chunk:
                current_chunk += "\n" + paragraph
            else:
                current_chunk = paragraph

        else:

            if current_chunk:
                chunks.append(current_chunk)

            # Preserve overlap
            overlap_text = current_chunk[-CHUNK_OVERLAP:]

            current_chunk = overlap_text + "\n" + paragraph

    # Save remaining content
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# ======================================
# 4. PROCESS ALL WEBSITE PAGES
# ======================================

def process_documents():

    print("\nStarting text preprocessing...\n")

    if not INPUT_FILE.exists():
        print("Input file not found:", INPUT_FILE)
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    all_chunks = []

    for document in documents:

        url = document["url"]
        title = document["title"]
        content = document["content"]

        # Clean content
        cleaned_content = clean_text(content)

        # Generate chunks
        chunks = split_into_chunks(cleaned_content)

        for index, chunk in enumerate(chunks):

            chunk_data = {
                "chunk_id": f"{url}#chunk-{index}",
                "url": url,
                "title": title,
                "chunk_index": index,
                "content": chunk,
                "content_length": len(chunk)
            }

            all_chunks.append(chunk_data)

    # Save processed chunks
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ==================================
    # 5. FINAL REPORT
    # ==================================

    print("=" * 50)
    print("PREPROCESSING COMPLETED")
    print("=" * 50)

    print("Total website pages:", len(documents))
    print("Total chunks generated:", len(all_chunks))
    print("Chunk size:", CHUNK_SIZE)
    print("Chunk overlap:", CHUNK_OVERLAP)

    print("Saved at:", OUTPUT_FILE.resolve())

    if all_chunks:

        print("\nFirst chunk preview:\n")
        print(all_chunks[0]["content"][:500])


# ======================================
# 6. PROGRAM ENTRY POINT
# ======================================

if __name__ == "__main__":
    process_documents()
