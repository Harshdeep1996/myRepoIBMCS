import requests
import tempfile
import os
import shutil
from collections import namedtuple


FileTuple = namedtuple('FileTuple', ['url', 'name'])


def fetch(file_tuple):
    r = requests.get(file_tuple.url)
    r.raise_for_status()
    path = os.path.join(tempfile.gettempdir(), file_tuple.name)

    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    return path
