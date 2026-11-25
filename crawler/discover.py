
import requests
import xml.etree.ElementTree as ET

from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser


# Our website
BASE_URL = "https://www.skilllearningacademy.com/"

# Maximum number of pages to discover
MAX_PAGES = 50

# Identify our crawler
HEADERS = {
    "User-Agent": "SkillLearningAcademyBot/1.0 (Website Knowledge Assistant)"
}

session = requests.Session()
session.headers.update(HEADERS)


def get_domain(url):
    """Return a normalized domain name."""
    domain = urlparse(url).netloc.lower()
    return domain.removeprefix("www.")


def normalize_url(url):
    """Remove fragments and normalize URLs."""
    url, _ = urldefrag(url)
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return None

    if parsed.path.lower().endswith(
        (".pdf", ".jpg", ".jpeg", ".png", ".gif",
         ".zip", ".doc", ".docx", ".mp4")
    ):
        return None

    # Ignore query parameters for our first version
    clean_url = parsed._replace(query="", fragment="")

    return clean_url.geturl().rstrip("/") or BASE_URL


def is_internal(url):
    """Check whether the URL belongs to our website."""
    return get_domain(url) == get_domain(BASE_URL)


def get_robots_parser():
    """Read the website's crawling permissions."""
    robots_url = urljoin(BASE_URL, "/robots.txt")

    response = session.get(robots_url, timeout=15)

    if response.status_code in (401, 403):
        raise RuntimeError(
            "Website robots.txt access is restricted."
        )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(response.text.splitlines())

    return parser


def get_sitemaps():
    """Discover sitemap URLs from robots.txt and common locations."""
    sitemap_urls = set()

    robots_url = urljoin(BASE_URL, "/robots.txt")

    try:
        response = session.get(robots_url, timeout=15)

        if response.status_code == 200:
            for line in response.text.splitlines():
                if line.lower().startswith("sitemap:"):
                    sitemap_urls.add(line.split(":", 1)[1].strip())

    except requests.RequestException as error:
        print("Could not read robots.txt:", error)

    sitemap_urls.add(urljoin(BASE_URL, "/sitemap.xml"))

    return sitemap_urls


def extract_sitemap_urls(sitemap_url):
    """Extract URLs from a sitemap or sitemap index."""
    discovered = set()

    try:
        response = session.get(sitemap_url, timeout=20)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        # Remove XML namespace from tag names
        for element in root.iter():
            if element.tag.endswith("loc") and element.text:
                link = element.text.strip()

                if link.endswith(".xml"):
                    discovered.update(
                        extract_sitemap_urls(link)
                    )
                else:
                    clean = normalize_url(link)

                    if clean and is_internal(clean):
                        discovered.add(clean)

    except Exception as error:
        print(f"Sitemap error ({sitemap_url}): {error}")

    return discovered


def extract_links(page_url, robots):
    """Extract internal links from one webpage."""
    links = set()

    if robots and not robots.can_fetch(HEADERS["User-Agent"], page_url):
        print("Blocked by robots.txt:", page_url)
        return links

    try:
        response = session.get(page_url, timeout=20)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type.lower():
            return links

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup.find_all("a", href=True):
            absolute_url = urljoin(page_url, tag["href"])
            clean_url = normalize_url(absolute_url)

            if clean_url and is_internal(clean_url):
                links.add(clean_url)

    except requests.RequestException as error:
        print(f"Page error ({page_url}): {error}")

    return links


def discover_pages():
    """Discover all permitted internal website pages."""
    print("\nStarting website discovery...\n")

    robots = get_robots_parser()
    sitemap_urls = get_sitemaps()

    # First, discover pages using sitemaps
    pages = set()

    for sitemap in sitemap_urls:
        pages.update(extract_sitemap_urls(sitemap))

    # Always include homepage
    homepage = normalize_url(BASE_URL)
    pages.add(homepage)

    # Then discover additional pages using internal links
    queue = deque(pages)
    visited = set()

    while queue and len(visited) < MAX_PAGES:
        current_url = queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        print(f"[{len(visited)}] Checking: {current_url}")

        new_links = extract_links(current_url, robots)

        for link in new_links:
            if link not in visited and link not in queue:
                if len(visited) + len(queue) < MAX_PAGES:
                    queue.append(link)

    return sorted(visited)


if __name__ == "__main__":
    discovered_pages = discover_pages()

    print("\n" + "=" * 50)
    print("WEBSITE DISCOVERY COMPLETED")
    print("=" * 50)

    for index, page in enumerate(discovered_pages, start=1):
        print(f"{index}. {page}")

    print(f"\nTotal discovered pages: {len(discovered_pages)}")

    # Save discovered URLs
    with open("data/discovered_urls.txt", "w", encoding="utf-8") as file:
        for page in discovered_pages:
            file.write(page + "\n")

    print("\nURLs saved to data/discovered_urls.txt")
