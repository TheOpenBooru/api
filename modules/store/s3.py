from modules import settings
from .base import BaseStore
import io
import boto3
from pathlib import Path

class S3Store(BaseStore):
    def __init__(self):
        s3_resource = boto3.resource('s3',
            aws_access_key_id=settings.AWS_ID,
            aws_secret_access_key=settings.AWS_SECRET,
            region_name=settings.AWS_REGION,
        )
        self.s3 = boto3.client('s3',
            aws_access_key_id=settings.AWS_ID,
            aws_secret_access_key=settings.AWS_SECRET,
            region_name=settings.AWS_REGION,
        )
        
        logged_in = self._check_login()
        if not logged_in:
            self.usable = False
            self.fail_reason = "Could not connect to AWS, check your credentials"
            return

        try:
            self._create_bucket()
        except Exception:
            self.usable = False
            self.fail_reason = "Could not create S3 Bucket"
            return
        
        self.usable = True
        self.bucket = s3_resource.Bucket(settings.STORAGE_S3_BUCKET)

    
    def _check_login(self) -> bool:
        try:
            self.s3.list_buckets()
        except Exception:
            return False
        else:
            return True

    def _create_bucket(self):
        buckets = self.s3.list_buckets()
        bucket_names = [x['Name'] for x in buckets['Buckets']]
        if settings.STORAGE_S3_BUCKET not in bucket_names:
            self.s3.create_bucket(
                Bucket=settings.STORAGE_S3_BUCKET,
                ACL='public-read',
                CreateBucketConfiguration={"LocationConstraint": settings.AWS_REGION}
            )
    
    def put(self, data:bytes, filename:str):
        self.put
        if type(data) != bytes:
            raise TypeError("Data wasn't bytes")
        buf = io.BytesIO(data)
        try:
            self.s3.upload_fileobj(
                buf, settings.STORAGE_S3_BUCKET,filename,
                ExtraArgs={"ACL":"public-read"}
            )
        except Exception:
            raise FileExistsError("The file already exists")


    def get(self, filename:str) -> bytes:
        buf = io.BytesIO()
        try:
            self.s3.download_fileobj(
                settings.STORAGE_S3_BUCKET,
                filename,
                buf
            )
        except Exception:
            raise FileNotFoundError("Key doesn't exist")
        else:
            return buf.getvalue()


    def exists(self, filename:str):
        """TODO: Don't donwload files to check existance"""
        try:
            self.get(filename)
        except FileNotFoundError:
            return False
        else:
            return True


    def url(self, filename:str) -> str:
        TEMPLATE = "https://{bucket}.s3.{region}.amazonaws.com/{filename}"
        return TEMPLATE.format(
            bucket=settings.STORAGE_S3_BUCKET,
            region=settings.AWS_REGION,
            filename=filename,
        )


    def delete(self, filename:str):
        try:
            self.s3.delete_object(
                Bucket=settings.STORAGE_S3_BUCKET,
                Key=filename,
            )
        except Exception:
            pass # Shouldn't error if key doesn't exist


    def clear(self):
        self.bucket.objects.all().delete()