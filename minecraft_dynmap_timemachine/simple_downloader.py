import requests
import logging
import binascii

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
}

dict = { # entry for nether need to be added
    "worldflat": 1,
    "worldt": 2,
    "world_the_endflat": 5,
    "world_the_endst": 6

}

def download(url, binary=False):
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


def dbdownload(url, mycursor, table):
    if not "z" in url.split("/")[5].replace(".png", "").split("_")[0]:
        x, y = url.split("/")[5].replace(".png", "").split("_")
        MapID = dict[url.split("/")[2] + url.split("/")[3]]
        mycursor.execute(
            f"SELECT NewImage FROM `%s`.`Tiles` WHERE x = %s AND y = %s AND MapID = %s AND zoom = 0;" % (table, x, y, MapID))
        for x in mycursor:
            return x[0]
    else:
        zoom = len(url.split("/")[5].replace(".png", "").split("_")[0])
        x = url.split("/")[5].replace(".png", "").split("_")[1]
        y = url.split("/")[5].replace(".png", "").split("_")[2]

        MapID = dict[url.split("/")[2] + url.split("/")[3]]
        mycursor.execute(
            f"SELECT NewImage FROM `%s`.`Tiles` WHERE x = %s AND y = %s AND MapID = %s AND zoom = %s;" % (table, x, y, MapID, zoom))
        for x in mycursor:
            return x[0]