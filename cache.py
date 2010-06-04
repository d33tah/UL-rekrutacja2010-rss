#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from time import time
import pysqlite2.dbapi2 as sqlite3

def cache_get(filename, url, frequency=30):
  
  now = int(time())

  #open the db and re-initialize it if needed
  conn = sqlite3.connect(filename)
  c = conn.cursor()
  c.execute("CREATE TABLE IF NOT EXISTS cache " + \
	      "(url TEXT UNIQUE, value TEXT, lasttime TEXT)")
  
  #look for the entry for a given url. check its time, use the data if correct
  entry = c.execute("SELECT * FROM cache WHERE url = ?", (url,) ).fetchone()
  if entry:
    if now - int(entry[2]) < frequency:
      page = entry[1]
    else:
      page = urllib.urlopen(url).read().decode('utf-8')
      c.execute("UPDATE cache SET lasttime = ?, value = ?" \
		+ "WHERE url = ?", (now,page,url))
      conn.commit()
  else:
    page = urllib.urlopen(url).read().decode('utf-8')
    c.execute("INSERT INTO cache VALUES (?,?,?)", (url,page,now))
    conn.commit()
  
  return page