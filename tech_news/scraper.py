from parsel import Selector
import requests
import time


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.ReadTimeout:
        return None
    if response.status_code != 200:
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    news = Selector(text=html_content).css(
        ".tec--list.tec--list--lg a.tec--card__title__link::attr(href)"
        ).getall()
    return news


# Requisito 3
def scrape_next_page_link(html_content):
    next_page_url = Selector(text=html_content).css(
        "a.tec--btn::attr(href)").get()
    if next_page_url is None:
        return None
    return next_page_url


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("#js-article-title::text").get()
    timestamp = selector.css("time::attr(datetime)").get()
    writer = (
        selector.css("#js-author-bar div p *::text").get()
        or selector.css(".z--font-bold a::text").get()
    ).strip()
    shares_count = int(
        selector.css(".tec--toolbar__item::text").re_first(r"\d+") or 0)
    comments_count = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+") or 0
        )
    summary = ''.join(
        selector.css(
            "div.tec--article__body > p:nth-of-type(1) *::text"
            ).getall())
    sources = selector.css("div.z--mb-16 a::text").getall()
    for source in range(len(sources)):
        sources[source] = sources[source].strip()
    categories = selector.css("#js-categories a.tec--badge::text").getall()
    for category in range(len(categories)):
        categories[category] = categories[category].strip()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories
    }


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
