import urllib.request
import urllib.parse
import urllib.error
import logging
import binascii

headers = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')
]

def download(url, binary=False):
    opener = urllib.request.build_opener()
    opener.addheaders = headers

    logging.info('download: %s', url)
    response = opener.open(url)
    data = response.read()
    if binary:
        # data = binascii.unhexlify(data)
        pass
    else:
        data = data.decode('utf-8')

    logging.info('length: %.2f KB', len(data) / 1000.0)
    logging.debug('content: %s', data)

    return data
