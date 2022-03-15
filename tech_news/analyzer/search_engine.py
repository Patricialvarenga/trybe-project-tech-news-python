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
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
