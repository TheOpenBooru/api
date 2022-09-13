from PIL.Image import Image
import imagehash
import numpy as np

def phash(image: Image) -> bytes:
    # Image hash returns a 2d array of booleans, 8x8
    im_hash = imagehash.average_hash(image,8)
    # Pack each 8 row into a numpy uint8, creating 8 unit8s
    flattened = np.packbits(im_hash.hash)
    # Convert the flattened array into bytes
    data = flattened.tobytes()
    return data
