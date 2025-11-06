"""
Gather content from various web sources.
"""
import os
import re
import requests
from bs4 import BeautifulSoup
from slugify import slugify
import openai
from .arxivit import action_gather_arxiv
from .get_youtube import action_gather_youtube
from .repo_rst import action_gather_repo

# TODO: Replace with a secure method for API key management
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")


def _download_and_summarize_url(url):
    """Downloads and summarizes a generic URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find("main") or soup.find("article") or soup.find("body")
    title = soup.find("title").get_text()

    for elem in main_content.select("script, style, meta, [document], head, title"):
        elem.extract()

    folder_name = slugify(title)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(os.path.join(folder_name, "original.html"), "w", encoding="utf-8") as file:
        file.write(str(main_content))

    # Summarization logic would go here.
    # For now, we're just saving the content.

    os.system(
        f"pandoc {os.path.join(folder_name, 'original.html')} -f html -t rst -s -o {os.path.join(folder_name, 'original.rst')}"
    )
    print(f"Web page content saved to {folder_name}.")
    return f"Content from {url} saved in folder {folder_name}"


def _fetch_wikipedia_content(subject):
    """Fetches content from Wikipedia."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": subject,
        "format": "json",
        "prop": "text",
        "redirects": "",
    }
    response = requests.get(url, params=params)
    data = response.json()
    raw_html = data["parse"]["text"]["*"]
    soup = BeautifulSoup(raw_html, "html.parser")
    text = ""
    for p in soup.find_all("p"):
        text += p.text
    
    folder_name = slugify(subject)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(os.path.join(folder_name, f"{folder_name}.txt"), "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Wikipedia content for '{subject}' saved to {folder_name}.")
    return f"Content for '{subject}' from Wikipedia saved in folder {folder_name}"


def action_gather_url(url: str):
    """
    Gathers content from a URL, intelligently handling the source.
    """
    if "wikipedia.org" in url:
        subject = url.split("/")[-1]
        return _fetch_wikipedia_content(subject)
    elif "arxiv.org" in url:
        paper_id = url.split("/")[-1]
        return action_gather_arxiv(paper_id)
    elif "youtube.com" in url or "youtu.be" in url:
        video_id = url.split("/")[-1]
        if 'v=' in video_id:
            video_id = video_id.split('v=')[-1]
        return action_gather_youtube(video_id)
    elif "github.com" in url:
        repo = "/".join(url.split("/")[-2:])
        return action_gather_repo(repo)
    else:
        return _download_and_summarize_url(url)

if __name__ == "__main__":
    test_url = input("Enter a URL to gather: ")
    action_gather_url(test_url)