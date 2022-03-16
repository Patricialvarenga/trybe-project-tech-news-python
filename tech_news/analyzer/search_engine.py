from tech_news.database import db
import re as yes
from datetime import datetime


# Requisito 6
# https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
def search_by_title(title):
    title_list = []
    t = yes.compile(title, yes.IGNORECASE)
    search_title = db.news.find({"title": {"$regex": t}})
    for titles in search_title:
        title_list.append((titles["title"], titles["url"]))
    return title_list


# Requisito 7
# https://docs.python.org/pt-br/3/library/datetime.html
def search_by_date(date):
    date_list = []
    search_date = db.news.find({"timestamp": {"$regex": date}})

    try:
        datetime.fromisoformat(date)

        for dates in search_date:
            date_list.append((dates["title"], dates["url"]))
        return date_list

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
# https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
def search_by_source(source):
    source_list = []
    s = yes.compile(source, yes.IGNORECASE)
    search_source = db.news.find({"sources": {"$regex": s}})
    for sources in search_source:
        source_list.append((sources["title"], sources["url"]))
    return source_list


# Requisito 9
# https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
def search_by_category(category):
    category_list = []
    c = yes.compile(category, yes.IGNORECASE)
    search_category = db.news.find({"categories": {"$regex": c}})
    for categories in search_category:
        category_list.append((categories["title"], categories["url"]))
    return category_list
