"""Tests for `aws-lambda-event-models` package."""

import pytest

from aws_lambda_event_models import EventSource, S3EventRecord


@pytest.fixture()
def s3_lambda_event(s3_event_record):
    return {
        "Records": [s3_event_record],
    }


@pytest.fixture()
def s3_event_record():
    """S3 Event from https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html"""
    return {
         "eventVersion":"2.1",
         "eventSource":"aws:s3",
         "awsRegion":"us-west-2",
         "eventTime":"1970-01-01T00:00:00.000Z",
         "eventName":"ObjectCreated:Put",
         "userIdentity":{
            "principalId":"AIDAJDPLRKLG7UEXAMPLE"
         },
         "requestParameters":{
            "sourceIPAddress":"127.0.0.1"
         },
         "responseElements":{
            "x-amz-request-id":"C3D13FE58DE4C810",
            "x-amz-id-2":"FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
         },
         "s3":{
            "s3SchemaVersion":"1.0",
            "configurationId":"testConfigRule",
            "bucket":{
               "name":"mybucket",
               "ownerIdentity":{
                  "principalId":"A3NL1KOZZKExample"
               },
               "arn":"arn:aws:s3:::mybucket"
            },
            "object":{
               "key":"HappyFace.jpg",
               "size":1024,
               "eTag":"d41d8cd98f00b204e9800998ecf8427e",
               "versionId":"096fKKXTRTtl3on89fVO.nfljtsv6qko",
               "sequencer":"0055AED6DCD90281E5"
            }
         }
      }


def test_correctly_parse_valid_s3_event_record(s3_event_record):
    """Test an S3 Event Record from AWS can be parsed into a Pydantic model."""
    record = S3EventRecord(**s3_event_record)
    assert '2.1' == record.event_version
    assert 'aws:s3' == record.event_source and EventSource.s3 == record.event_source
