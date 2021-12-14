import os
import io
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def put(data:bytes, name:str) -> bool:
    buf = io.BytesIO(data)
    try:
        response = s3.upload_fileobj(buf,f'distrubutor', name)
    except ClientError as e:
        print(e)
        return False
    else:
        return True

def get(name:str) -> bytes:
    buf = io.BytesIO()
    try:
        s3.download_fileobj(f'distrubutor', name, buf)
        return buf.getvalue()
    except:
        raise FileNotFoundError("Attempted to Get Non-Existant File")

def delete(name:str) -> bool:
    try:
        response = s3.delete_object(f'distrubutor',Key=name)
    except ClientError as e:
        return False
    else:
        return True