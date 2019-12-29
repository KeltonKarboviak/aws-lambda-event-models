"""Top-level package for aws-lambda-event-models."""

from base64 import b64decode
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


__author__ = """Kelton Karboviak"""
__email__ = "kelton.karboviak@gmail.com"
__version__ = "0.0.1"


class Base64Str(str):
    """base64 encoded data validation."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (bytes, str)):
            raise TypeError(f'bytes or string required, received {type(v)}')
        decoded = b64decode(v).decode('utf8')
        return cls(decoded)

    def __repr__(self):
        return f'Base64({super().__repr__()})'


class EventSource(str, Enum):
    kinesis = "aws:kinesis"
    s3 = "aws:s3"


class Kinesis(BaseModel):
    schema_version: str
    partition_key: str
    sequence_number: str
    approximate_arrival_timestamp: datetime
    data: str
    decoded_data: Base64Str = None

    class Config:
        fields = {
            "schema_version": "kinesisSchemaVersion",
            "partition_key": "partitionKey",
            "sequence_number": "sequenceNumber",
            "approximate_arrival_timestamp": "approximateArrivalTimestamp",
            'decoded_data': 'data',
        }


class KinesisEventRecord(BaseModel):
    event_version: str
    event_source: EventSource
    aws_region: str
    event_name: str
    event_id: str
    event_source_arn: str
    kinesis: Kinesis

    class Config:
        fields = {
            "event_version": "eventVersion",
            "event_source": "eventSource",
            "aws_region": "awsRegion",
            "event_name": "eventName",
            "event_id": "eventID",
            "event_source_arn": "eventSourceARN",
        }


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
        fields = {"etag": "eTag", "version_id": "versionId"}


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
