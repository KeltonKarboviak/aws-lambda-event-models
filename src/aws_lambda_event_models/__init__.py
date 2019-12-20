"""Top-level package for aws-lambda-event-models."""

from enum import Enum

from pydantic import BaseModel


__author__ = """Kelton Karboviak"""
__email__ = 'kelton.karboviak@gmail.com'
__version__ = '0.0.1'


class EventSource(str, Enum):
    s3 = 'aws:s3'


class S3EventRecord(BaseModel):
    event_version: str
    event_source: EventSource

    class Config:
        fields = {'event_version': 'eventVersion', 'event_source': 'eventSource'}
