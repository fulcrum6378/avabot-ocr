import base64
from cgi import FieldStorage
from io import BytesIO
import os.path
from sys import argv

from PIL import Image

root = os.path.dirname(__file__)
picture: Image = None
post_get = "p"

if __name__ == "__main__":
    if len(argv[1:]) > 0:
        picture = Image.open(os.path.join(root, argv[1]))
    else:
        got = {post_get: ""}
        try:
            for g in FieldStorage().list: got[g.name] = g.value
        except:
            pass
        if got[post_get] == "":
            raise Exception("Did not receive any data!")
        picture = BytesIO(base64.b64decode(got[post_get]))
