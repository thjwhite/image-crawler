import requests
import sys
from bs4 import BeautifulSoup
import os
import errno
import time
import sqlite3

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
    nextLink = None
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
                nextLink = href
    return nextLink

if __name__ == '__main__':
    url = raw_input('Enter the URL: ')
    while True :
        url = process_page(url)
