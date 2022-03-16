# parsel é uma biblioteca utilizada para extrair dados de um conteúdo web
from parsel import Selector
# requests é uma biblioteca HTTP
import requests
import time
from tech_news.database import create_news


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
# o link para várias paginas de notícia
# está no atributo href em um elemento âncora (<a>)
# que possue a classe tec--card__title
# que possue a classe tec--list tec--list--lg
def scrape_novidades(html_content):
    news = Selector(text=html_content).css(
        ".tec--list.tec--list--lg a.tec--card__title__link::attr(href)"
        ).getall()
    return news


# Requisito 3
# o link para a próxima pagina
# está no atributo href em um elemento âncora <a>
# que possue a classe tec--btn
def scrape_next_page_link(html_content):
    next_page_url = Selector(text=html_content).css(
        "a.tec--btn::attr(href)").get()
    if next_page_url is None:
        return None
    return next_page_url


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
# url: está no atributo href com um atributo <rel=canonical>, em um link
    url = selector.css("link[rel=canonical]::attr(href)").get()
# title: está no texto possui o id js-article-title
    title = selector.css("#js-article-title::text").get()
# timestamp: está no atributo datetime q possue o time
    timestamp = selector.css("time::attr(datetime)").get()
# writer: ou pego todo texto da tag ancestral e e de suas tags descendentes
# dentro de um p que está dentro de uma div
# que possui o id js-author-bar
# ou faço o strip do texto q contém o elemento <a>
# que está na classe z--font--bold
    writer = (
        selector.css("#js-author-bar div p *::text").get()
        or selector.css(".z--font-bold a::text").get()
    ).strip()
# shares_count: pego o text(int para transformar para inteiro o número)
# q está dentro da classe tec--toolbar e substituo o get pelo re_first
# para além de reupera os valores tbm aplicar a expressão regular sobre ele
    shares_count = int(
        selector.css(".tec--toolbar__item::text").re_first(r"\d+") or 0)

    comments_count = int(
        selector.css("#js-comments-btn::text").re_first(r"\d+") or 0)
# sumary: de td texto das tag ancestral e tags descendentes
# pego o primeiro parágrafo q está dentro da div tec--article__body
# faço join para unir tds as strings
    summary = ''.join(
        selector.css(
            "div.tec--article__body > p:nth-of-type(1) *::text"
            ).getall())

# sources: está no texto q contém o elemento <a>
# dentro da div z--mb-16
# como é uma lista, preciso percorrer todo conteúdo e fazer o strip
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
    html_content = fetch("https://www.tecmundo.com.br/novidades")
    news_urls = scrape_novidades(html_content)

    for _ in range(amount):
        new_page_url = scrape_next_page_link(html_content)
        next_content = fetch(new_page_url)
        news_urls = news_urls + scrape_novidades(next_content)

    news_urls = news_urls[:amount]
    news_scraped_list = []

    for news_url in news_urls:
        news_page_html_content = fetch(news_url)
        news_scraped_data = scrape_noticia(news_page_html_content)
        news_scraped_list.append(news_scraped_data)

    create_news(news_scraped_list)
    return news_scraped_list
