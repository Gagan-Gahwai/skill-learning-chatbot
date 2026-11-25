
import json
import time

from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_URL = "https://www.skilllearningacademy.com/"

URLS_FILE = Path("data/discovered_urls.txt")
OUTPUT_DIR = Path("data/raw")

OUTPUT_FILE = OUTPUT_DIR / "website_content.json"
FAILED_FILE = OUTPUT_DIR / "failed_urls.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
}


# ==========================================
# 2. SAVE DATA SAFELY
# ==========================================

def save_json(data, file_path):
    """
    Save JSON data safely using a temporary file.
    """

    temp_file = file_path.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    temp_file.replace(file_path)


# ==========================================
# 3. EXTRACT WEBSITE CONTENT
# ==========================================

def extract_page_content(page, url):
    """
    Open a webpage using Playwright,
    execute JavaScript and extract readable text.
    """

    print(f"\nExtracting: {url}")

    try:

        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        if response is None:
            print("No response received.")
            return None

        print("Status Code:", response.status)

        if response.status >= 400:
            print("HTTP error:", response.status)
            return None

        # Wait for JavaScript-rendered content
        try:
            page.wait_for_function(
                """
                () => {
                    const root = document.querySelector('#root');
                    return root && root.innerText.trim().length > 0;
                }
                """,
                timeout=15000
            )

        except PlaywrightTimeoutError:
            print("Warning: JavaScript content wait timed out.")

        # Give the page a little more time to render
        page.wait_for_timeout(1500)

        # Get rendered HTML
        html = page.content()

        soup = BeautifulSoup(html, "lxml")

        # Extract title
        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        # Remove unnecessary HTML elements
        for tag in soup([
            "script",
            "style",
            "noscript",
            "iframe",
            "svg"
        ]):
            tag.decompose()

        # Find the most relevant content container
        main_content = (
            soup.find("main")
            or soup.find("article")
            or soup.find(id="root")
            or soup.body
        )

        if main_content is None:
            print("No readable content container found.")
            return None

        # Extract text
        text = main_content.get_text(
            separator="\n",
            strip=True
        )

        # Clean empty lines
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        clean_text = "\n".join(lines)

        # Check useful content
        if len(clean_text) < 50:
            print("Very little text found.")
            return None

        # Prepare structured data
        page_data = {
            "url": url,
            "title": title,
            "content": clean_text,
            "content_length": len(clean_text)
        }

        print("Title:", title)
        print("Extracted characters:", len(clean_text))

        return page_data

    except Exception as error:

        print("Extraction failed:", error)
        return None


# ==========================================
# 4. SCRAPE ALL DISCOVERED URLS
# ==========================================

def scrape_all_pages():

    print("\nStarting website scraping...\n")

    # Check URL file
    if not URLS_FILE.exists():
        print("URL file not found:", URLS_FILE)
        return

    # Read discovered URLs
    with open(URLS_FILE, "r", encoding="utf-8") as file:

        urls = list(dict.fromkeys(
            line.strip()
            for line in file
            if line.strip()
        ))

    print("Total URLs discovered:", len(urls))

    if not urls:
        print("No URLs available for scraping.")
        return

    all_pages = []
    failed_urls = []

    # Start browser
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            extra_http_headers=HEADERS
        )

        # Process every URL
        for index, url in enumerate(
            tqdm(urls, desc="Scraping website"),
            start=1
        ):

            print(f"\nPage {index}/{len(urls)}")

            page_data = extract_page_content(
                page,
                url
            )

            if page_data:

                all_pages.append(page_data)

            else:

                failed_urls.append({
                    "url": url,
                    "reason": "Extraction failed or insufficient content"
                })

            # Save progress after every URL
            save_json(all_pages, OUTPUT_FILE)
            save_json(failed_urls, FAILED_FILE)

            # Respect the website's server
            time.sleep(1)

        browser.close()

    # ======================================
    # 5. FINAL REPORT
    # ======================================

    print("\n" + "=" * 55)
    print("WEBSITE SCRAPING COMPLETED")
    print("=" * 55)

    print("Total URLs:", len(urls))
    print("Successfully extracted:", len(all_pages))
    print("Failed URLs:", len(failed_urls))

    print("\nSaved files:")

    print("Website content:", OUTPUT_FILE.resolve())
    print("Failed URLs:", FAILED_FILE.resolve())

    print("\nScraping process finished!")


# ==========================================
# 6. PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    scrape_all_pages()
