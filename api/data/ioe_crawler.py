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
        
        notices = []
        
        
        
        for td in tds:
            # tds[0] -> s.no  ,tds[1] -> title  , tds[2] -> notice date
            if td.css('td::text').get() in i:
                title = tds[tds.index(td)+1].css('span::text').get()
                url = str(response.url).split('/?')[0][:-1] + str(tds[tds.index(td)+1].css('a::attr(href)').get())
                date = tds[tds.index(td)+2].css('td::text').get()
                notices.append({'title':title, 'url':url, 'date':date})
        
        with open('api/data/new_notices.json','w') as file:
            json.dump(notices, file, indent = 4)

        #next_page = response.css('li.PagedList-skipToNext a::attr(href)').get()
        
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
