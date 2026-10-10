import base64
import io
from PIL import Image,UnidentifiedImageError

MAX_PAGES=5
MAX_IMAGE=3*1024*1024
MAX_TOTAL=3*1024*1024

def verify_image(raw):
    if len(raw)>MAX_IMAGE: raise ValueError('Image must be under 3 MB.')
    try:
        image=Image.open(io.BytesIO(raw))
        if image.format not in ['JPEG','PNG'] or image.width*image.height>20_000_000: raise ValueError('Use JPEG/PNG up to 20 megapixels.')
        mime='image/png' if image.format=='PNG' else 'image/jpeg'
        image.verify()
        return raw,mime
    except (UnidentifiedImageError,OSError,Image.DecompressionBombError) as exc:
        raise ValueError('An image could not be read.') from exc

def decode_pages(data):
    encoded=data.get('image_pages')
    if encoded is None: encoded=[data['image_data']] if data.get('image_data') else []
    if not isinstance(encoded,list) or len(encoded)>MAX_PAGES: raise ValueError('Upload at most 5 pages of one invoice.')
    pages=[]
    for value in encoded:
        if not isinstance(value,str): raise ValueError('Invalid image data.')
        pages.append(verify_image(base64.b64decode(value,validate=True)))
    if sum(len(raw) for raw,_ in pages)>MAX_TOTAL: raise ValueError('Invoice images must be under 3 MB combined.')
    return pages
