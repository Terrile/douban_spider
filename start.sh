mkdir jobcache
scrapy crawl bookspider -s JOBDIR=jobcache --logfile=bookspider.log
#update the JOBDIR para according to http://stackoverflow.com/questions/27943970/how-to-limit-scrapy-request-objects
#according the refered url, the main purpose of jobdir is to limit the request num reside in memory