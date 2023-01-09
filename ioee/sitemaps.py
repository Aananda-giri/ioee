# ioee/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from code_share.models import Code
import math

# class BlogPostSitemap(Sitemap):
#     changefreq = "weekly"

#     def items(self):
#         return AddedJokes.objects.all()

# class StaticViewSitemap(Sitemap):
#     changefreq = 'monthly'

#     def items(self):
#         return ['code', 'chat', 'Register']

#     def location(self, item):
#         return reverse(item)

class EachCodeViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Code.objects.all()
        #return ['home']

    #def location(self, item):
    #    return reverse(item)

class CodeHomePageViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0


    def items(self):
        max_pages = math.ceil(Code.objects.all().count()/10)
        pages = []
        for page in range(1,max_pages):
            pages.append(f'/{page}/')

        return pages

    def location(self, item):
        return f'{item}'
    