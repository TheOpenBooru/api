import os
import io
import boto3 as _boto3
from botocore.exceptions import ClientError as _ClientError

_BUCKET_NAME = 'openbooru'
_s3 = _boto3.client('s3')

# ToDo: Create the bucket automatically
# _boto3.client('s3').create_bucket(
#     Bucket=_BUCKET_NAME,
#     ACL='public-read',
#     CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
# )

def put(key:str,data:bytes):
    """Saves the data to a key
    
    Raises:
        FileExistsError: Name Already Exists
    """
    buf = io.BytesIO(data)
    try:
        _s3.upload_fileobj(buf, _BUCKET_NAME, key,ExtraArgs={'ACL':'public-read'})
    except _ClientError as e:
        raise FileExistsError("Name Already Exists")

def get(key:str) -> bytes:
    """Get data from it's key

    Raises:
        FileNotFoundError: File does not exist
    """
    buf = io.BytesIO()
    try:
        _s3.download_fileobj(_BUCKET_NAME, key, buf)
        return buf.getvalue()
    except:
        raise FileNotFoundError("Attempted to Get Non-Existant File")


def url(key:str) -> str:
    """Generate a file URL from it's key

    Raises:
        FileNotFoundError: File does not exist
    """
    return f"https://{_BUCKET_NAME}.s3.eu-west-2.amazonaws.com/{key}"

def delete(key:str):
    "Delete the file from it's key"
    try:
        _s3.delete_object(Bucket=_BUCKET_NAME,Key=key)
    except _ClientError as e:
        pass
