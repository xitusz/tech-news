from tech_news.database import search_news
import re
from datetime import datetime


# Requisito 6
def search_by_title(title):
    news = search_news({"title": re.compile(title, re.IGNORECASE)})

    return [(item["title"], item["url"]) for item in news]


# Requisito 7
def search_by_date(date):
    try:
        old_date = datetime.strptime(date, "%Y-%m-%d")

        formated_date = datetime.strftime(old_date, "%d/%m/%Y")

        news = search_news({"timestamp": formated_date})
    except ValueError:
        raise ValueError("Data inválida")

    return [(item["title"], item["url"]) for item in news]


# Requisito 8
def search_by_tag(tag):
    news = search_news({"tags": re.compile(tag, re.IGNORECASE)})

    return [(item["title"], item["url"]) for item in news]


# Requisito 9
def search_by_category(category):
    news = search_news({"category": re.compile(category, re.IGNORECASE)})

    return [(item["title"], item["url"]) for item in news]
