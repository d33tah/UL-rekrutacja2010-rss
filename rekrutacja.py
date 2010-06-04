#!/usr/bin/python
# -*- coding: utf-8 -*-

from cache import cache_get
from lxml import html
from datetime import datetime
import PyRSS2Gen

def application(environ, start_response):
  
  url = 'https://rekrutacja.uni.lodz.pl/index.php?op=news'
  tree = html.fromstring(cache_get('cache.sqlite',url))
    
  rss = PyRSS2Gen.RSS2(
  title = "Rekrutacja UŁ - aktualności",
  link = "http://deetah.jogger.pl",
  description = "Kanał zawiera aktualności ze strony rekrutacja.uni.lodz.pl",
  )
  
  for item in tree.xpath('//table'):
    date_raw = item[1].text_content()[:item[1].text_content().find(',')]
    day = tuple(int(a) for a in date_raw.split(' ')[0].split('-'))
    hour = tuple(int(a) for a in date_raw.split(' ')[1].split(':')) 
    
    rss_title = item[0][0][0].text_content()
    rss_description = item[2][0][0].text_content() 
    rss_pubDate = datetime( *(day+hour) )
    
    rss.items.append( PyRSS2Gen.RSSItem(
		      title = rss_title,
		      description = rss_description,
		      link = url,
		      guid = PyRSS2Gen.Guid( rss_description ),
		      pubDate = rss_pubDate
		    ))

  start_response('200 OK', [('Content-type','application/rss+xml')])
  return rss.to_xml(encoding='utf-8')

if __name__ == '__main__':
  print application()