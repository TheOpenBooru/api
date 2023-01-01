from openbooru.modules import settings
from .base import BaseStore
import io
import boto3

class S3Store(BaseStore):
    _bucket_name:str
    usable: bool = False
    def __init__(self, bucket_name = settings.STORAGE_S3_BUCKET):
        self._bucket_name = bucket_name
        if bucket_name == "":
            self.fail_reason = "S3 Bucket Name was not set in settings"
            return
        
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
            self.fail_reason = "Could authenticate AWS correctly, check your credentials or permissions."
            return

        try:
            self._create_bucket(bucket_name)
        except Exception as e:
            self.fail_reason = f"Could not create S3 Bucket, A bucket with that name may already exist. Try changing it.\n {e}"
            return
        
        self.usable = True
        self.bucket = s3_resource.Bucket(bucket_name)

    
    def _check_login(self) -> bool:
        try:
            self.s3.list_buckets()
        except Exception:
            return False
        else:
            return True

    def _create_bucket(self,bucket_name:str):
        buckets = self.s3.list_buckets()
        bucket_names = [x['Name'] for x in buckets['Buckets']]
        if bucket_name not in bucket_names:
            self.s3.create_bucket(
                Bucket=bucket_name,
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
                buf,
                self._bucket_name,
                filename,
                ExtraArgs={"ACL":"public-read"}
            )
        except Exception as e:
            raise FileExistsError("The file already exists")


    def get(self, filename:str) -> bytes:
        buf = io.BytesIO()
        try:
            self.s3.download_fileobj(
                self._bucket_name,
                filename,
                buf
            )
        except Exception:
            raise FileNotFoundError("Key doesn't exist")
        else:
            return buf.getvalue()


    def exists(self, filename:str):
        try:
            self.get(filename)
        except FileNotFoundError:
            return False
        else:
            return True


    def url(self, filename:str) -> str:
        TEMPLATE = "https://{bucket}.s3.{region}.amazonaws.com/{filename}"
        return TEMPLATE.format(
            bucket=self._bucket_name,
            region=settings.AWS_REGION,
            filename=filename,
        )


    def delete(self, filename:str):
        try:
            self.s3.delete_object(
                Bucket=self._bucket_name,
                Key=filename,
            )
        except Exception:
            pass # Shouldn't error if key doesn't exist


    def clear(self):
        self.bucket.objects.all().delete()