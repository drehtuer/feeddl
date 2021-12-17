"""
"""

from __future__ import print_function
import Feed
import sys
import json
import DownloadFilter
import Downloader


def stdout(*args):
    print(*args, file=sys.stdout)


def stderr(*args):
    print(*args, file=sys.stderr)


class FeedDl:

    _FEEDDL_VERSION='0.0.1'


    def __init__(self, config):
        self._config = config
        self._parseConfig()


    def _parseConfig(self):
        with open(self._config, 'r') as f:
            self._config = json.load(f)


    @staticmethod
    def version():
        return FeedDl._FEEDDL_VERSION
    

    def download(self, args):
        downloadFilter = DownloadFilter.DownloadFilter(self._config['data'])
        downloader = Downloader.Downloader(self._config)
        for dl in self._config['feeds']:
            print('Checking \'{}\''.format(dl['name']))
            try:
                feed = Feed.Feed(dl['url'])
                newEntries = downloadFilter.filterNew(dl['name'], feed.entries())
                print('\tNew entries: {}/{}'.format(len(newEntries), len(feed.entries())))

                for entry in newEntries:
                    if downloader.download(dl, entry, args.dryrun):
                        downloadFilter.update(dl['name'], entry)
            except Exception as e:
                print('\t{}'.format(e),
                        file = sys.stderr)

    def feeds(self, args):
        for feed in self._config['feeds']:
            stdout('[{}]'.format(feed['name']))
            stdout('\tURL: {}'.format(feed['url']))
            stdout('\tLatest entry: {}'.format('TODO'))


    def raw(self, args):
        url = None
        for feed in self._config['feeds']:
            if args.name == feed['name']:
                url = feed['url']
        if url is None:
            stderr('No feed named \'{}\''.format(args.name))
            sys.exit(1)

        stdout(Feed.Feed(url))


    def episodes(self, args):
        url = None
        for feed in self._config['feeds']:
            if args.name == feed['name']:
                url = feed['url']
        if url is None:
            stderr('No feed named \'{}\''.format(args.name))
            sys.exit(1)

        try:
            feed = Feed.Feed(url)
            header = feed.header()
            stdout('Feed: \'{}\''.format(header['title']))
            if 'link' in header:
                stdout('Link: {}'.format(header['link']))
            stdout('Updated: {}'.format(feed.updated()))
            stdout('Episodes:')
            for entry in feed.entries():
                stdout('\tTitle: \'{}\''.format(entry['title']))
                if 'published' in entry:
                    stdout('\t\tPublished: {}'.format(feed.parseDate(entry['published_parsed'])))
                if 'subtitle' in entry:
                    stdout('\t\tSubtitle: {}'.format(entry['subtitle']))
        except Exception as e:
            print('\t{}'.format(e),
                    file = sys.stderr)
