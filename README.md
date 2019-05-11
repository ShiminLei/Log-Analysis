# Description

Python script uses psycopg2 to query a PostgreSQL database for a news website, and print out the result for given questions.

# Requirements

1. Virtual machine - [Vagrant](https://www.vagrantup.com/) (config from [Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)).
2. [VirtualBox](https://www.virtualbox.org/)
3. PostgreSQL
4. Python3

# Data

newsdata.sql from the [link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

# Problems solved

1. What are the most popular three articles of all time?
2.  Who are the most popular article authors of all time?
3.  On which days did more than 1% of requests lead to errors?

# Setup

1. `vagrant up`  to start up the virtual machine.
2.  `vagrant ssh` to log into the virtual machine.
3. `psql -d news -f newsdata.sql` in vagrant directory to load the data and create the tables.
4. Create views according to [Views created](#view).
5. `python code.py` to print out the result.

# <span id="view">Views created</span>

```sql
create view article_author as
select authors.name, articles.title, articles.slug
from articles, authors
where articles.author = authors.id;
```

```sql
create view date_status as
select date(time), status 
from log 
```

```sql
create view fail_status as 
select date, count(*) 
from date_status
where status like '%404%'
group by date;
```

```sql
create view total_status as 
select date, count(*) 
from date_status
group by date;
```

```sql
create view fail_total as 
select total_status.date, 
total_status.count as total_count,
fail_status.count as fail_count,
fail_status.count::numeric/total_status.count::numeric as perc
from fail_status join total_status 
on fail_status.date = total_status.date;
```



