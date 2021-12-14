import io
import numpy as np
from PIL import Image

def encodeToJPEG(img:bytes) -> bytes:
    img = Image.open(img)
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.read()

def downscale(img:bytes,target:int) -> bytes:
    """
    Args:
        img (bytes): img in a bytes format
        target (int): target megapixels for downscale
    Returns:
        bytes: returns the bytes of a jpeg image
    """
    buf = io.BytesIO(img)
    PILimg = Image.open(buf)
    
    width = PILimg.width
    height = PILimg.height
    MPs = width * height
    if MPs > target:
        factor = MPs / target
        res = (width//factor, height//factor)
        PILimg = PILimg.resize(res)
    
    buf = io.BytesIO()
    PILimg.save(buf,'JPEG')
    content = buf.read()
    
    return content
