# Program 4: Scrapy
**Due**: Thursday, September 25, 2025, 11:59 PM  

Use the website that you selected in consultation with me, or contact me if you're having trouble using the concepts discussed so far to access its content.

 
For this programming assignment you will be graded on your ability to use Scrapy to crawl your website. Find at least one "start url" and follow links to accumulate at least 100 "item" pages and use Scrapy's "xpath" or "css" search function to find at least 10 attributes for each item page. "Yield" the data from each item page as a dictionary and use the command line arguments to save those to a "JSON lines" file (*.jl).
 
The following represent the expectations to earn a B on this assignment.  You will need to do more to earn an A:

* Use 'scrapy' to scrape pages ethically following the robots.txt and using a delay between downloading pages

* Yield at least least 100 item pages

* Use CSS or XPATH select statements (response.css or response.xpath)

* Yield a dictionary with at least 10 attributes from each item page

* In addition to your Scrapy project, submit a JSON lines file containing your data.

To earn an A, you might:
* scrape more types of pages/items

* scrape more attributes per item 
* accumulate different item types to different files
* something else that increased the difficulty level of the assignment.

Submit a ZIP file containing your scrapy project directory (with scrapy.cfg) to asulearn.  You may need to remove the ".scrapy" folder that includes the httpcache folder if you used caching.
 
In comments at the top of your spider Python file include the following:
* your name

* links to the resources you used

* Describe the additional work that you did to exceed the requirements for a B