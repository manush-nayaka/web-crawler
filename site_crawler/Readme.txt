What does this crawler do?
    This crawler scrapes the site "http://quotes.toscrape.com/" for the quotes and also all the links from each page it can visit(I am using "igraph" to do this)

Dependencies:
    Have tested the code in python3.5 as the crawler is implemented in scrapy. To install python3.5 in linux please visit "https://tecadmin.net/install-python-3-5-on-ubuntu/". To install the python dependencies please run from commanline "pip install requirements.txt".

Folder structure and Files:
    site_crawler --- The main project folder
        --> crawl.sh -- to run the crawler
        --> requirements.txt -- python dependencies for the project
        --> scrapy.cgf -- scrapy configuration to run from the deployment
        --> scripts 
                --> installation.sh --  installation script for debian platforms
                --> parse_links.py -- script to view graphical representation of links someone visit across pages (uses igraph)
        --> test -- unit tests run "python3.x -m unittest"
        --> scraped_data -- contains all the scraped data
        --> log -- contains log from the crawler

        --> site_crawler -- crawler project folder, to match scrapy folder structure
            --> setting.py -- contains all the setting related to politeness parameters, pipelines
            --> middlewares.py
            --> pipelines.py -- 2 classes to support pipelines in the project
            --> items.py -- items used in the pipeline 
            --> spiders
                --> quotes_spider.py -- the actual crawler used in the project

To Run: execute crawl.sh shell script

Questions to follow up from the assignment.
1. Can this crawler be made even more generic, i.e. can it handle other sites with different html layouts? 
    Please document how you would this in README. Lastly extend the code above to incorporate this.
    Yes it can be made generic just by inheriting the SpiderWeb class and rewriting the parse method would make it implement to any html layout
    
2. Are there any sites you cannot crawl?
    The answer to this is yes aswell as no. If the site admin decides to block the bots he can do it, there are several reasons one of them is to limit traffic by the bots. 

3. How would you scale this crawler so it can crawl millions of website?
    The framework supports braod crawling functionality. Also we could have microservice to partition the start urls from where the focused crawling can be used to scale this.

4. How would you store all the different data?
    Here in the project we are storing the data to disk using the 2 pipelines but the data can be stored to other storage engines as the framework supports

5. Explain the architecture and design of the system. Draw a simple diagram if time permits
    The class "SpiderWeb" in the quotes_spider.py is the class responsible for crawling. It starts by calling the method start_requests which acts as seed url to start the crawling (returns a generator of requests to be scheduled the scrapy scheduler picks up this generator function and schedules the requests). 

    The seed/scheduled requests before being sent to the server goes through request middlewares(one of them is duplicate elimination requests and dropping cross domain requests used in the project). 
    
    The request sending and receiving is async call(the scrapy uses the twisted network framework which is event driven network IO)

    The request sending can be prioritised, throttled(16 concurent request per domain) for further improvement for controlling the request flow
. After the reception of response, the download manager calls the callback registered for the particular request. 
    
    In the parser callback the parsing logic and the elements of interests are extracted using the item template(2 item templates are used in here QuotesItem and WebLinkItem please refer item.py file) which basically maps elements in the download html page to the items and further the parser schedules requests from the current parsed web page.
    
    There are 2 pipelines used in this system, QuoteItem are moved to QuotesItemPipeline and WeblinkItem to WebLinkUrlPipeline. The 2 pipeline takes care of how data should stream to different sink.

    The best diagram to explain the working of differnt components is to refer the scrapy framework documentation (https://docs.scrapy.org/en/latest/topics/architecture.html)

6. Explain the data model
    I am using simple structure to write the scraped data, the style of writing is append only at the end of the crawling. All the data goes into the scraped_data folder from 2 pipelines. The quotes folder contains all the quotes segregated to each author with filename as author name and the links extracted from the url line pipeline has TCSV style of writing to the file.    

7. Explain the design patterns used
    Observer pattern -- for the event driven network IO
    Generator pattern -- for scheduling requests
    
