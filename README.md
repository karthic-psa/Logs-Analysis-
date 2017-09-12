In this project we build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like. The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity. The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

Here, we will be interacting with a live database both from the command line and from your code. We will explore a large database with over a million rows and will build and refine complex queries and use them to draw business conclusions from data.

Building an informative summary from logs is a real task that comes up very often in software engineering. 

In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

This shows one of the valuable roles of a database server in a real-world application: it's a point where different pieces of software (a web app and a reporting tool, for instance) can share data.

Reports to be generated:

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer back to this lesson if you want to review the idea of HTTP status codes.)


How to Run:

1. Download the data and launch your Vagrant machine (and cd into the required directory).

2. To load the data, use the command psql -d news -f newsdata.sql.

3. Connect to the database and explore the data
-> To connect to the data base use the following command: psql -d news 

4. Create the required VIEWS.
-> Use the following SQL Queries to create the required VIEWS: 

	CREATE VIEW authorarticles AS SELECT art.title, art.slug, aut.name FROM articles art, authors aut WHERE aut.id=art.authors ORDER BY aut.name; 

	CREATE VIEW noofviewsmain AS SELECT path, status, COUNT(*) AS views FROM log GROUP BY path, status HAVING status = '200 OK' ORDER BY views;

	CREATE VIEW viewsofarticlesmain AS SELECT authorarticles.name, authorarticles.title, noofviewsmain.views FROM authorarticles, noofviewsmain 
	WHERE noofviewsmain.path = CONCAT('/article/', authorarticles.slug) ORDER BY authorarticles.name;

	CREATE VIEW noofrequests AS SELECT count(*) AS totalreq, date(TIME) AS dates FROM log GROUP BY dates ORDER BY totalreq DESC;

	CREATE VIEW nooferrors AS SELECT count(*) AS totalerr, date(TIME) AS dates FROM log WHERE status='404 NOT FOUND' GROUP BY dates ORDER BY totalerr DESC;

	CREATE VIEW errorpercent AS SELECT noofrequests.dates, round((100.0*nooferrors.totalerr)/noofrequests.totalreq,2) AS percentage_error FROM nooferrors, noofrequests WHERE nooferrors.dates=noofrequests.dates;

5. Run the command 'python logAnalysis.py' in the vagrant command line.
