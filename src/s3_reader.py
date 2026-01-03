from __future__ import annotations

import boto3
import json

from config import S3_BUCKET
from interfaces import Reader


class S3Reader(Reader):

    def __init__(self, client=None, default_bucket: str = S3_BUCKET):
        self._client = client or boto3.client("s3")
        self._default_bucket = default_bucket

    def read(self, event: dict[str, any]) -> dict[str, any]:
        bucket = event.get("bucket", self._default_bucket)
        key = event["key"]
        
        obj = self._client.get_object(Bucket=bucket, Key=key)
        return json.loads(obj["Body"].read())