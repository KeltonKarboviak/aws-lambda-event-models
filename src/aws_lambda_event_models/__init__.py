"""Top-level package for aws-lambda-event-models."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


__author__ = """Kelton Karboviak"""
__email__ = "kelton.karboviak@gmail.com"
__version__ = "0.0.1"


class EventSource(str, Enum):
    s3 = "aws:s3"


class S3Bucket(BaseModel):
    name: str
    arn: str


class S3Object(BaseModel):
    key: str
    size: int
    etag: str
    version_id: str
    sequencer: str

    class Config:
        fields = {
            "etag": "eTag",
            "version_id": "versionId",
        }


class S3(BaseModel):
    schema_version: str
    bucket: S3Bucket
    object: S3Object

    class Config:
        fields = {"schema_version": "s3SchemaVersion"}


class S3EventRecord(BaseModel):
    event_version: str
    event_source: EventSource
    aws_region: str
    event_time: datetime
    event_name: str
    s3: S3

    class Config:
        fields = {
            "event_version": "eventVersion",
            "event_source": "eventSource",
            "aws_region": "awsRegion",
            "event_time": "eventTime",
            "event_name": "eventName",
        }
