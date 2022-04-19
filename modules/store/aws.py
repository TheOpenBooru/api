from modules import settings
import io
import hashlib
import boto3
from boto3.resources import factory

s3 = boto3.resource(
    's3',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ID,
    aws_secret_access_key=settings.AWS_SECRET,
)
bucket = s3.Bucket(settings.STORAGE_BUCKET)

try:
    bucket.create(
        ACL="public-read",
        CreateBucketConfiguration={"LocationConstraint": settings.AWS_REGION},
    )
except Exception:
    pass

def put(data: bytes,suffix:str = "",prefix:str = "") -> str:
    """Raises:
    - TypeError: Data wasn't bytes

    Returns: Key(str): ID for the data
    """
    if type(data) != bytes:
        raise TypeError("Data wasn't bytes")
    hash = hashlib.sha3_256(data).hexdigest()
    key = prefix + hash + suffix

    buf = io.BytesIO(data)
    bucket.upload_fileobj(
        buf, key,
        ExtraArgs={"ACL":"public-read"}
    )
    return key


def get(key: str) -> bytes:
    """Raises:
    FileNotFoundError: Key doesn't exist
    """
    buf = io.BytesIO()
    try:
        bucket.download_fileobj(key, buf)
    except Exception:
        raise FileNotFoundError("Key doesn't exist")
    return buf.getvalue()


def url(key: str) -> str:
    template = "https://{bucket}.s3.{region}.amazonaws.com/{key}"
    return template.format(
        bucket=settings.STORAGE_BUCKET,
        region=settings.AWS_REGION,
        key=key,
    )


def delete(key: str):
    try:
        bucket.delete_objects(
            Delete={
                'Objects': [
                    {'Key': key}
                ],
                'Quiet': True
            }
        )
    except Exception:
        pass # Shouldn't error if key doesn't exist


def clear():
    ...