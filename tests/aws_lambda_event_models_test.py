"""Tests for `aws-lambda-event-models` package."""

from datetime import datetime, timezone

import pytest

from aws_lambda_event_models import EventSource, KinesisEventRecord, S3EventRecord


@pytest.fixture()
def s3_lambda_event(s3_event_record):
    return {
        "Records": [s3_event_record],
    }


@pytest.fixture()
def kinesis_event_record():
    """Kinesis Event from https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html"""
    return {
        "kinesis": {
            "kinesisSchemaVersion": "1.0",
            "partitionKey": "1",
            "sequenceNumber": "49590338271490256608559692538361571095921575989136588898",
            "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0Lg==",
            "approximateArrivalTimestamp": 1545084650.987,
        },
        "eventSource": "aws:kinesis",
        "eventVersion": "1.0",
        "eventID": "shardId-000000000006:49590338271490256608559692538361571095921575989136588898",
        "eventName": "aws:kinesis:record",
        "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-role",
        "awsRegion": "us-east-2",
        "eventSourceARN": "arn:aws:kinesis:us-east-2:123456789012:stream/lambda-stream",
    }


@pytest.fixture()
def s3_event_record():
    """S3 Event from https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html"""
    return {
        "eventVersion": "2.1",
        "eventSource": "aws:s3",
        "awsRegion": "us-west-2",
        "eventTime": "1970-01-01T00:00:00.000Z",
        "eventName": "ObjectCreated:Put",
        "userIdentity": {"principalId": "AIDAJDPLRKLG7UEXAMPLE"},
        "requestParameters": {"sourceIPAddress": "127.0.0.1"},
        "responseElements": {
            "x-amz-request-id": "C3D13FE58DE4C810",
            "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD",
        },
        "s3": {
            "s3SchemaVersion": "1.0",
            "configurationId": "testConfigRule",
            "bucket": {
                "name": "mybucket",
                "ownerIdentity": {"principalId": "A3NL1KOZZKExample"},
                "arn": "arn:aws:s3:::mybucket",
            },
            "object": {
                "key": "HappyFace.jpg",
                "size": 1024,
                "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                "sequencer": "0055AED6DCD90281E5",
            },
        },
    }


def test_correctly_parse_valid_kinesis_event_record(kinesis_event_record):
    """Test an Kinesis Event Record from AWS can be parsed into a Pydantic model."""
    record = KinesisEventRecord(**kinesis_event_record)

    # top-level fields
    assert "1.0" == record.event_version
    assert (
        "aws:kinesis" == record.event_source
        and EventSource.kinesis == record.event_source
    )
    assert "us-east-2" == record.aws_region
    assert "aws:kinesis:record" == record.event_name
    assert (
        "shardId-000000000006:49590338271490256608559692538361571095921575989136588898"
        == record.event_id
    )
    assert (
        "arn:aws:kinesis:us-east-2:123456789012:stream/lambda-stream"
        == record.event_source_arn
    )

    # kinesis fields
    kinesis_metadata = record.kinesis
    assert "1.0" == kinesis_metadata.schema_version

    assert "1" == kinesis_metadata.partition_key
    assert (
        "49590338271490256608559692538361571095921575989136588898"
        == kinesis_metadata.sequence_number
    )
    assert "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0Lg==" == kinesis_metadata.data
    assert "Hello, this is a test." == kinesis_metadata.decoded_data
    assert (
        datetime(2018, 12, 17, 22, 10, 50, 987000, tzinfo=timezone.utc)
        == kinesis_metadata.approximate_arrival_timestamp
    )


def test_correctly_parse_valid_s3_event_record(s3_event_record):
    """Test an S3 Event Record from AWS can be parsed into a Pydantic model."""
    record = S3EventRecord(**s3_event_record)

    # top-level fields
    assert "2.1" == record.event_version
    assert "aws:s3" == record.event_source and EventSource.s3 == record.event_source
    assert "us-west-2" == record.aws_region
    assert datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc) == record.event_time
    assert "ObjectCreated:Put" == record.event_name

    # s3 fields
    s3_metadata = record.s3
    assert "1.0" == s3_metadata.schema_version

    assert "mybucket" == s3_metadata.bucket.name
    assert "arn:aws:s3:::mybucket" == s3_metadata.bucket.arn

    assert "HappyFace.jpg" == s3_metadata.object.key
    assert 1024 == s3_metadata.object.size
    assert "d41d8cd98f00b204e9800998ecf8427e" == s3_metadata.object.etag
    assert "096fKKXTRTtl3on89fVO.nfljtsv6qko" == s3_metadata.object.version_id
    assert "0055AED6DCD90281E5" == s3_metadata.object.sequencer
