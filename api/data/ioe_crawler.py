# -------------------------------------------------------------------------
#Change Format To: notices = [{'title':---, 'date':---, 'url':---} ,{...} ]
# -------------------------------------------------------------------------

import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
import json

class IoeSpider(scrapy.Spider):
    name = "ioe"
    start_urls = [
            'https://exam.ioe.edu.np/',
        ]
    def parse(self, response):
        tds = response.css('td')
        i=[str(a) for a in range(1,11)]
        
        #text of data
        texts=[]
        
        #url of data
        urls=[]
        
        
        
        for td in tds:
            if td.css('td::text').get() in i:
                texts.append(tds[tds.index(td)+1].css('span::text').get())
                urls.append(str(response.url).split('/?')[0][:-1] + str(tds[tds.index(td)+1].css('a::attr(href)').get()))
        
        with open('api/data/new_notices.json','w') as file:
            json.dump({'topics':texts, 'urls':urls}, file, indent = 4)
        #break
        #print('\n\n\n\n\n',{'topics':texts, 'urls':urls})
        #yield{'topics':texts, 'urls':urls}
        #next_page = response.css('li.PagedList-skipToNext a::attr(href)').get()
        
        #with open('data.json','w') as file:
        #    json.dump({'texts':texts, 'urls':urls}, file, indent = 4)
        
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)







# the wrapper to make it run more times
def run_spider():
    def f(q):
        try:
            spider=IoeSpider
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            #q.put(e)
            pass
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    #p.stop()

    if result is not None:
        raise result

#run_spider()


  
#get_new_notifications()
