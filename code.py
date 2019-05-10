#!/usr/bin/env python
import psycopg2

# query_1 = """
# select articles.title, count(*) as counts
# from log join articles
# on substr(log.path, 10) = articles.slug
# group by title
# order by counts desc
# limit 3;
# """

# 以下方法更好，因为Consider news website distinct sections: article, sporttv, artists...
query_1 = """
select articles.title, count(*) as counts
from log join articles
on log.path = CONCAT('/article/', articles.slug)
group by title
order by counts desc
limit 3;
"""


query_2 = """
select name, count(*) as counts
from article_author, log
where slug = substr(log.path, 10)
group by name
order by counts desc
"""

query_3 = """
select date, perc from fail_total
where perc>0.01;
"""


def process(query):
    db = psycopg2.connect(database="news")
    cur = db.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    db.close()
    return rows


def question1(query=query_1):
    rows = process(query)
    print("The most popular three articles of all time are:")
    for row in rows:
        print('"{}" -- {} views'.format(row[0], row[1]))
    print('\n\n')


def question2(query=query_2):
    rows = process(query)
    print("The most popular authors of all time are:")
    for row in rows:
        print('"{}" -- {} views'.format(row[0], row[1]))
    print('\n\n')


def question3(query=query_3):
    rows = process(query)
    print("Days did more than 0.01 of requests lead to errors are:")
    for date, div in rows:
        print('{} -- {:.2%}  errors'.format(date, div))
    print('\n\n')


if __name__ == '__main__':
    question1()
    question2()
    question3()
