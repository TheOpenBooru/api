from modules import settings
import io
import hashlib
import boto3
from boto3.resources import factory

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ID,
    aws_secret_access_key=settings.AWS_SECRET,
    region_name=settings.AWS_REGION,
)

def is_logged_in() -> bool:
    try:
        s3.list_buckets()
    except Exception:
        return False
    else:
        return True

if is_logged_in():
    buckets = s3.list_buckets()
    bucket_names = [x['Name'] for x in buckets['Buckets']]
    if settings.STORAGE_S3_BUCKET not in bucket_names:
        s3.create_bucket(
            Bucket=settings.STORAGE_S3_BUCKET,
            ACL='public-read',
            CreateBucketConfiguration={"LocationConstraint": settings.AWS_REGION}
        )

def put(data: bytes,suffix:str="") -> str:
    """Raises:
    - TypeError: Data wasn't bytes

    Returns: Key(str): ID for the data
    """
    if type(data) != bytes:
        raise TypeError("Data wasn't bytes")
    key = hashlib.sha3_256(data).hexdigest()
    key += suffix
    buf = io.BytesIO(data)
    s3.upload_fileobj(
        buf, settings.STORAGE_S3_BUCKET,key,
        ExtraArgs={"ACL":"public-read"}
    )
    return key


def get(key: str) -> bytes:
    """Raises:
    FileNotFoundError: Key doesn't exist
    """
    buf = io.BytesIO()
    try:
        s3.download_fileobj(settings.STORAGE_S3_BUCKET, key, buf)
    except Exception:
        raise FileNotFoundError("Key doesn't exist")
    return buf.getvalue()


def url(key: str) -> str:
    template = "https://{bucket}.s3.{region}.amazonaws.com/{key}"
    return template.format(
        bucket=settings.STORAGE_S3_BUCKET,
        region=settings.AWS_REGION,
        key=key,
    )


def delete(key: str):
    try:
        s3.delete_object(
            Bucket=settings.STORAGE_S3_BUCKET,
            Key=key,
        )
    except Exception:
        pass # Shouldn't error if key doesn't exist


def clear():
    ...
