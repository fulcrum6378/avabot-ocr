import base64
from cgi import FieldStorage
from io import BytesIO
import json
import os.path
from sys import argv
from typing import Optional

from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cmc
from colormath.color_objects import AdobeRGBColor, LabColor, sRGBColor
import numpy as np
from PIL import Image

root = os.path.dirname(__file__)
image: Image = None
post_get = "p"
is_adobe_rgb = lambda img: 'Adobe RGB' in img.info.get('icc_profile', '')

if len(argv[1:]) > 0:
    image = Image.open(os.path.join(root, argv[1]))
else:
    got = {post_get: ""}
    try:
        for g in FieldStorage().list: got[g.name] = g.value
    except:
        pass
    if got[post_get] == "":
        raise Exception("Did not receive any data!")
    image = Image.open(BytesIO(base64.b64decode(got[post_get])))

# First rows then columns (549 x 166)
colourType = AdobeRGBColor if is_adobe_rgb(image) else sRGBColor
data: np.ndarray = np.asarray(image)
lab: Optional[np.ndarray] = None
for x in data:
    xLab: Optional[np.ndarray] = None
    for y in x:
        con = convert_color(colourType(y[0], y[1], y[2], is_upscaled=True), LabColor)
        if xLab is None:
            xLab = np.array(con, ndmin=1)
        else:
            xLab = np.append(xLab, con)
    if lab is None:
        lab = np.array(xLab, ndmin=2)
    else:
        lab = np.append(lab, [xLab], axis=0)

# with open(os.path.join(root, "exported.json"), "w") as f:
#    f.write(json.dumps(data.tolist(), indent=2))
print(lab)
print(lab.shape)
# white = convert_color(sRGBColor(255, 255, 255, is_upscaled=True), LabColor)
# black = convert_color(sRGBColor(0, 0, 0, is_upscaled=True), LabColor)
# delta_e_cmc(black, black)
