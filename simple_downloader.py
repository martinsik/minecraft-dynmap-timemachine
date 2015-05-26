import urllib.request
import urllib.parse
import urllib.error
import logging
from urllib.error import HTTPError
import binascii

headers = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')
]

def download(url, binary=False):
    opener = urllib.request.build_opener()
    opener.addheaders = headers

    logging.debug('download: %s', url)

    try:
        response = opener.open(url)
    except HTTPError as e:
        logging.debug('Server error code %d with: %s', e.code, e.msg)
        raise e

    data = response.read()
    if binary:
        # data = binascii.unhexlify(data)
        pass
    else:
        data = data.decode('utf-8')
        logging.debug('content: %s', data)

    logging.debug('length: %.2f KB', len(data) / 1000.0)

    return data
