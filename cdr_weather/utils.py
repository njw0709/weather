import urllib.request


def download_file(url, destfile):
    urllib.request.urlretrieve(url, destfile)
