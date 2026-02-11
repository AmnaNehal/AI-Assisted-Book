import re
import uuid
import asyncio
import httpx
from bs4 import BeautifulSoup

from config.settings import settings
from core.answer_generator import AnswerGenerator
from db.qdrant_client import QdrantConnector


BASE_URL = "https://book-creation-using-ai.vercel.app"

# Docusaurus docs/blog ko crawl karne ke liye start pages
START_PATHS = [
    "/docs/",
    "/blog",
]

# kuch links ignore
IGNORE_PREFIXES = (
    "mailto:",
    "tel:",
    "javascript:",
)

def clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s

def is_internal_link(href: str) -> bool:
    if not href:
        return False
    if href.startswith(IGNORE_PREFIXES):
        return False
    if href.startswith("http"):
        return href.startswith(BASE_URL)
    return href.startswith("/")

def normalize_url(href: str) -> str:
    if href.startswith("http"):
        return href.split("#")[0]
    return (BASE_URL + href).split("#")[0]

def extract_main_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")

    title = soup.title.get_text(strip=True) if soup.title else "Untitled"

    # Docusaurus usually has <main> ... <article>
    main = soup.find("main")
    if not main:
        main = soup.body

    # Try article first
    article = main.find("article") if main else None
    container = article if article else main

    text = container.get_text(" ", strip=True) if container else soup.get_text(" ", strip=True)

    # remove some common nav/footer noise
    junk_phrases = [
        "Skip to main content",
        "Copyright",
        "Built with Docusaurus",
    ]
    for j in junk_phrases:
        text = text.replace(j, " ")

    return clean_text(title), clean_text(text)

def chunk_text_simple(text: str, max_chars: int = 1400, overlap: int = 200):
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

async def fetch_html(client: httpx.AsyncClient, url: str) -> str:
    r = await client.get(url, timeout=30)
    r.raise_for_status()
    return r.text

async def crawl_site(max_pages: int = 60):
    visited = set()
    queue = [BASE_URL + p for p in START_PATHS]
    pages = []

    async with httpx.AsyncClient(headers={"User-Agent": "BookRAGBot/1.0"}) as client:
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            try:
                html = await fetch_html(client, url)
            except Exception:
                continue

            title, text = extract_main_text(html)

            # docs/blog pages only (filter out home template pages if needed)
            if "/docs" in url or "/blog" in url:
                pages.append({"url": url, "title": title, "text": text})

            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a"):
                href = a.get("href")
                if not is_internal_link(href):
                    continue
                full = normalize_url(href)
                if ("/docs" in full or "/blog" in full) and full not in visited and full not in queue:
                    queue.append(full)

    return pages

async def main():
    print("✅ Crawling website...")
    pages = await crawl_site(max_pages=80)
    print(f"✅ Pages found: {len(pages)}")

    ag = AnswerGenerator()
    qd = QdrantConnector()

    all_points = []
    book_id = "website_book"

    for page in pages:
        # text me title + body combine
        combined = f"{page['title']}\n\n{page['text']}"
        chunks = chunk_text_simple(combined, max_chars=1400, overlap=200)

        for idx, ch in enumerate(chunks):
            emb = await ag.generate_embedding(ch)
            all_points.append({
                "id": str(uuid.uuid4()),
                "content": ch,
                "embedding": emb,
                "book_id": book_id,
                "chunk_index": idx,
                "metadata": {
                    "source_url": page["url"],
                    "page_title": page["title"],
                }
            })

    print(f"✅ Total chunks to upload: {len(all_points)}")

    # Qdrant me insert
    await qd.insert_chunks(all_points)

    print("✅ Done. Qdrant ingest complete.")

if __name__ == "__main__":
    asyncio.run(main())