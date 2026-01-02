"""
S3Reader implementation following SRP, OCP, LSP, and DIP.
SRP: Only responsible for reading from S3.
OCP: Can extend with other readers (FileReader, KafkaReader) without modification.
LSP: Can substitute any Reader implementation.
DIP: Depends on boto3 client abstraction, can be injected.
"""
from __future__ import annotations

import boto3
import json

from config import S3_BUCKET
from interfaces import Reader


class S3Reader(Reader):
    """
    Reads JSON data from AWS S3.
    Following SRP: Single responsibility of S3 data retrieval.
    """

    def __init__(self, client=None, default_bucket: str = S3_BUCKET):
        """
        Initialize S3 reader.
        
        Args:
            client: boto3 S3 client (injectable for testing).
            default_bucket: Default bucket to use if not specified in event.
        """
        self._client = client or boto3.client("s3")
        self._default_bucket = default_bucket

    def read(self, event: dict[str, any]) -> dict[str, any]:
        """
        Read JSON from S3.
        
        Args:
            event: Must contain 'key', optionally 'bucket'.
            
        Returns:
            Parsed JSON as dictionary.
        """
        bucket = event.get("bucket", self._default_bucket)
        key = event["key"]
        
        obj = self._client.get_object(Bucket=bucket, Key=key)
        return json.loads(obj["Body"].read())