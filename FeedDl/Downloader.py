import os
import urllib
import re
import stagger
from stagger.id3 import *
import time
import sys
import subprocess

FORMATER_REGEX = re.compile(r'.*(%[^%]+%).*')
SANITIZE_FILENAME = str.maketrans('','','<>:"/\\|?*')

class Downloader:


    def __init__(self, config):
        self._config = config
        os.makedirs(self._config['download'], exist_ok=True)


    def _downloadDir(self, feed):
        return os.path.join(self._config['download'], feed['download'])


    def _formatName(self, feed, formaters, entity):
        formaters.update(entity)
        filename = feed['filename']
        found = True
        while found:
            match = FORMATER_REGEX.match(filename)
            if match:
                key = match.group(1)
                if key[1:-1] in formaters:
                    filename = filename.replace(key, formaters[key[1:-1]])
                else:
                    filename = filename.replace(key, '???')
            else:
                found = False
        filename = filename.translate(SANITIZE_FILENAME)
        return filename


    def _writeTags(self, feed, filename, formaters):
        tagdict = { }
        for tag, value in feed['tag'].items():
            found = True
            while found:
                match = FORMATER_REGEX.match(value)
                if match:
                    key = match.group(1)
                    if key[1:-1] in formaters:
                        value = value.replace(key, formaters[key[1:-1]])
                    else:
                        value = value.replace(key, '')
                else:
                    found = False
            if value != '':
                tagdict[tag] = value
        stagger.util.set_frames(filename, tagdict)


    def download(self, feed, entity, dryrun):
        result = True
        for link in entity['links']:
            if 'rel' in link and link['rel'] == 'enclosure':
                    os.makedirs(self._downloadDir(feed), exist_ok=True)
                    filename_full = os.path.basename(link['href'])
                    filename, filename_ext = os.path.splitext(filename_full)
                    filename_ext = filename_ext.split('?')[0]
                    formaters = {
                        'filename_full': filename_full,
                        'filename': filename,
                        'filename_ext': filename_ext,
                        'date-filename':
                        time.strftime(self._config['date-filename'],
                            entity['published_parsed']),
                        'date-tag': time.strftime(self._config['date-tag'],
                            entity['published_parsed']),
                    }
                    formatedName = self._formatName(feed, formaters, entity)
                    print('\t\tDownloading \'{}\' as \'{}\''.format(filename_full, formatedName))
                
                    if not dryrun:
                        try:
                            with urllib.request.urlopen(url=link['href']) as f:
                                data = f.read()
                            absolute_filename = os.path.join(self._downloadDir(feed), formatedName)
                            with open(absolute_filename, 'wb') as f:
                                f.write(data)
                            if filename_ext.endswith('mp3'):
                                self._writeTags(feed, absolute_filename, formaters)
                            if 'notify' in self._config and self._config['notify']:
                                subprocess.run([self._config['notify'], 'Downloaded new eposode \'{}\''.format(absolute_filename)])
                        except Exception as e:
                            result = False
                            print(e)
        return result
