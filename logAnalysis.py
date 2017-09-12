#!/usr/bin/env python

import psycopg2


def connect():
    """Connect to the PostgreSQL database.
Returns a database connection."""
    try:
        return psycopg2.connect("dbname=news")
    except:
        print("Cannot conncet to DATABASE")


def popart():
    db = connect()
    cu = db.cursor()

    # Part 1
    query_one = """SELECT viewsofarticlesmain.title, viewsofarticlesmain.views
    FROM viewsofarticlesmain ORDER BY viewsofarticlesmain.views DESC LIMIT 3;
    """
    cu.execute(query_one)
    results_one = cu.fetchall()
    print "The most popular three articles of all time are: "
    for (t, v) in results_one:
        print("% s - %s views") % (t, v)

    # Part 2
    query_two = """SELECT viewsofarticlesmain.name, SUM(viewsofarticlesmain.
    views) AS page_views FROM viewsofarticlesmain GROUP BY
    viewsofarticlesmain.name ORDER BY page_views DESC;"""
    cu.execute(query_two)
    results_two = cu.fetchall()
    print "\nThe most popular article authors of all time are: "
    for (n, pv) in results_two:
        print("%s - %s views") % (n, pv)

    # Part 3
    query_three = """SELECT * FROM errorpercent WHERE
    errorpercent.percentage_error > 1	ORDER BY errorpercent.percentage_error
    DESC;"""
    cu.execute(query_three)
    results_three = cu.fetchall()
    print """\nDays On which there was more than 1% of errors: """
    for (d, pe) in results_three:
        print("%s - %s%% errors") % (d, pe)
    db.close()


if __name__ == "__main__":
    connect()
    popart()
