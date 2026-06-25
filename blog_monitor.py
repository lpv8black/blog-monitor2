"""
Blog Monitor for amdrodd.com/blog
Prints the latest blog post to the console.
"""

import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://amdrodd.com/blog"

def fetch_posts():
    headers = {"User-Agent": "Mozilla/5.0 (blog-monitor-bot)"}
    resp = requests.get(BLOG_URL, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = []
    for heading in soup.find_all(["h2", "h3"]):
        link = heading.find("a", href=True)
        if link and "amdrodd.com" in link["href"]:
            title = link.get_text(strip=True)
            url   = link["href"]
            if title:
                posts.append((title, url))
    return posts

def main():
    print(f"Checking {BLOG_URL} ...\n")
    posts = fetch_posts()
    if posts:
        title, url = posts[0]
        print("Latest blog post:")
        print(f"  Title : {title}")
        print(f"  URL   : {url}")
    else:
        print("No posts found.")

if __name__ == "__main__":
    main()
