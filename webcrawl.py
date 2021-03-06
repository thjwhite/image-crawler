import requests
from bs4 import BeautifulSoup
import os
import errno
import time
import Queue
from urlparse import urlparse, urlunparse
from database import ImageDatabase, IMG_TYPES, DATA_DIR, DATABASE_FILE


def download_and_save_file(url, filepath, db):
    r = requests.get(url)
    try:
        os.makedirs('/'.join(filepath.split('/')[0:-1]))
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    with open(filepath, 'wb+') as f:
        f.write(r.content)
    name = filepath.split('/')[-1]
    sess_time = filepath.split('/')[-2]
    db.create_image_entry(url, name, sess_time, len(r.content))


def process_page(url, db):
    print "Now processing: " + url
    t = str(int(time.time()))
    nextLinks = []
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            if href.split('.')[-1] in IMG_TYPES:
                print href
                download_and_save_file(
                    href, os.path.join(DATA_DIR, t, href.split('/')[-1]), db)
            elif link.string is not None and \
                link.string.strip().startswith('next'):
                    print link.string
                    nextLinks.append(href)
    db.inc_pages_crawled()
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


def main():
    db = ImageDatabase(DATABASE_FILE)
    url = raw_input('Enter the URL: ')
    url_queue = Queue.Queue()
    url_queue.put(fix_url(url))
    while not url_queue.empty():
        url = url_queue.get()
        if url is not None:
            newLinks = process_page(url, db)
            for l in newLinks:
                url_queue.put(l)
    print "No more 'next' links!"

if __name__ == '__main__':
    main()
