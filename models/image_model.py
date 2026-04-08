# models/image_model.py

import numpy as np


def is_artwork(image):
    arr = np.array(image)

    # detect if blank / useless
    if arr.std() < 8:
        return False

    return True


def extract_features(image):
    width, height = image.size

    # size detection
    if width < 500:
        size = "small"
    elif width < 1000:
        size = "medium"
    else:
        size = "large"

    # detail detection
    arr = np.array(image)
    detail = int(min(10, arr.std() / 20))

    return {
        "size": size,
        "detail_level": detail
    }