import base64
import os.path
from cgi import FieldStorage
from io import BytesIO
from sys import argv
from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cmc  # Delta E Equation
from colormath.color_objects import AdobeRGBColor, LabColor, sRGBColor

root = os.path.dirname(__file__)
image: Image = None
post_get = "p"
is_adobe_rgb = lambda img: 'Adobe RGB' in img.info.get('icc_profile', '')
colourType = AdobeRGBColor if is_adobe_rgb(image) else sRGBColor

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


def lab(col: Sequence):
    return convert_color(colourType(col[0], col[1], col[2], is_upscaled=True), LabColor)


data: np.ndarray = np.asarray(image)
anal: Optional[np.ndarray] = None
for x in range(len(data)):
    xAnal: Optional[np.ndarray] = None
    for y in range(len(data[x])):
        cell = data[x][y]
        cLab = lab(cell)
        dif = 0

        if x > 0: dif += delta_e_cmc(lab(data[x - 1][y]), cLab) * 0.05  # Vertical Comparison
        if y > 0: dif += delta_e_cmc(lab(data[x][y - 1]), cLab) * 0.05  # Horizontal Comparison

        if dif > 100: dif = 100
        res = [2.55 * dif, 2.55 * dif, 2.55 * dif]
        xAnal = np.array(res, ndmin=2) if xAnal is None else np.append(xAnal, [res], axis=0)
    anal = np.array(xAnal, ndmin=3) if anal is None else np.append(anal, [xAnal], axis=0)

plt.imshow(anal)
plt.show()
