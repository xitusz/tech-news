import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(
            url,
            headers={"user-agent": "Fake user-agent"},
            timeout=3,
        )

        time.sleep(1)

        if response.status_code == 200:
            return response.text

        return None
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)

    cards = selector.css(".entry-title a::attr(href)").getall()

    if not cards:
        return []

    return cards


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    next_page_url = selector.css(".next::attr(href)").get()

    if not next_page_url:
        return None

    return next_page_url


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    return {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css(".entry-title::text").get().strip(),
        "timestamp": selector.css(".meta-date::text").get(),
        "writer": selector.css(".author a::text").get(),
        "comments_count": len(selector.css(".post-comments").getall()),
        "summary": "".join(
            selector.css(".entry-content > p:nth-of-type(1) ::text").getall()
        ).strip(),
        "tags": selector.css(".post-tags a::text").getall(),
        "category": selector.css(".label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    BASE_URL = "https://blog.betrybe.com/"
    links = []
    news = []

    while len(links) <= amount:
        html_content = fetch(BASE_URL)

        for item in scrape_novidades(html_content):
            links.append(item)

        BASE_URL = scrape_next_page_link(html_content)

    for item in links[0:amount]:
        news.append(scrape_noticia(fetch(item)))

    create_news(news)

    return news
