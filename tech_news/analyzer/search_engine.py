from tech_news.database import db
import re as yes


# https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
def search_by_title(title):
    title_list = []
    t = yes.compile(title, yes.IGNORECASE)
    search_title = db.news.find({"title": {"$regex": t}})
    for titles in search_title:
        title_list.append((titles["title"], titles["url"]))
    return title_list


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
