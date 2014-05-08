import requests
import sys
from bs4 import BeautifulSoup
import os
import errno
import time
import sqlite3
import Queue
from urlparse import urlparse, urlunparse

img_types = ['jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff']
data_dir = os.path.join(os.path.expanduser('~'), 'webcrawled')

def download_and_save_file(url, filepath):
    r = requests.get(url)
    try:
        os.makedirs('/'.join(filepath.split('/')[0:-1]))
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    with open(filepath, 'wb+') as f:
        f.write(r.content)

def process_page(url):
    print "Now processing: " + url
    t = str(int(time.time()))
    nextLinks = []
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            if href.split('.')[-1] in img_types:
                print href
                download_and_save_file(
                    href, os.path.join(data_dir, t, href.split('/')[-1]))
            elif link.string is not None and 'next' in link.string:
                nextLinks.append(href)
    return nextLinks

def fix_url(url):
    scheme, netloc, path, params, query, fragment = urlparse(url, 'http')
    if netloc == '':
        if not path.startswith('www'):
            netloc = 'www.' + path
            path = ''
        else:
            netloc = path
            path = ''
    return urlunparse((scheme, netloc, path, params, query, fragment))

if __name__ == '__main__':
    url = raw_input('Enter the URL: ')
    url_queue = Queue.Queue()
    url_queue.put(fix_url(url))
    while not url_queue.empty():
        url = url_queue.get()
        if url is not None :
            for l in process_page(url):
                url_queue.put(l)
    print "No more 'next' links!"
