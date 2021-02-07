from __future__ import print_function
from datetime import datetime
import feedparser
import json


IGNORE_BOZO_EXCEPTIONS = [
    feedparser.exceptions.CharacterEncodingOverride,
]

class Feed:
   
    def __init__(self, url):
        self._feed = feedparser.parse(url)
        if self._feed.bozo:
            if type(self._feed.bozo_exception) not in IGNORE_BOZO_EXCEPTIONS:
                print('Feed error on line{}: \'{}\''.format(
                    self._feed.bozo_exception.getLineNumber(),
                    self._feed.bozo_exception.getMessage()),
                    file=sys.stderr
                )
        self._feed['bozo_exception'] = None


    def all(self):
        return self._feed


    def entries(self):
        return self._feed['entries']


    def header(self):
        return self._feed['feed']

    
    def updated(self):
        updated = '?'
        if 'updated_parsed' in self._feed:
            updated = self.parseDate(self._feed['updated_parsed'])
        elif 'entries' in self._feed:
            updated = self.parseDate(self._feed['entries'][0]['published_parsed'])
            for entry in self._feed:
                if 'published_parsed' in entry:
                    entry_date = self.parseDate(entry['published_parsed'])
                    if entry_date > updated:
                        updated = entry_date
        return updated


    def parseDate(self, published_parsed):
        return datetime(
            year=published_parsed.tm_year,
            month=published_parsed.tm_mon,
            day=published_parsed.tm_mday,
            hour=published_parsed.tm_hour,
            minute=published_parsed.tm_min,
            second=published_parsed.tm_sec
        )
        
    
    def __repr__(self):
        return json.dumps(self._feed, indent=4)
