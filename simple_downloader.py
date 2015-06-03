import requests
# import urllib.request
# import urllib.parse
# import urllib.error
import logging
# from urllib.error import HTTPError
import binascii

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
}

def download(url, binary=False):
    # opener = urllib.request.build_opener()
    # opener.addheaders = headers

    logging.debug('download: %s', url)

    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        if binary:
            # data = binascii.unhexlify(data)
            data = response.content
        else:
            response.encoding = 'utf8'
            data = response.text
            logging.debug('content: %s', data)

        logging.debug('length: %.2f KB', len(data) / 1000.0)
    else:
        raise Exception()

    return data
