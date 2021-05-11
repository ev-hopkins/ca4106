import os
import tempfile
import unittest
import boto3
from boto3 import client
import botocore
from moto import mock_s3
from funcs import uploadImages

MY_BUCKET = "testbucketca4106"
images = ['test0.jpg', 'test1.jpg', 'test2.jpg', 'test3.jpg', 'test4.jpg']


@mock_s3
class TestUploadImages(unittest.TestCase):

    def setUp(self):
        client = boto3.client(
            "s3",
            region_name="eu-west-1",
            # aws_access_key_id="AKIAVDMP3OANL5GRGASX",
            # aws_secret_access_key="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",
        )
        try:
            s3 = boto3.resource(
                "s3",
                region_name="eu-west-1",
                aws_access_key_id="AKIAVDMP3OANL5GRGASX",
                aws_secret_access_key="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",
            )
            s3.meta.client.head_bucket(Bucket=MY_BUCKET)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = "{bucket} should not exist.".format(bucket=MY_BUCKET)
            raise EnvironmentError(err)
        client.create_bucket(Bucket=MY_BUCKET, CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1',
        },)

    def tearDown(self):
        s3 = boto3.resource(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="AKIAVDMP3OANL5GRGASX",
            aws_secret_access_key="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",
        )
        bucket = s3.Bucket(MY_BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def test_uploadImages(self):
        uploadImages(images, MY_BUCKET)
        conn = client('s3')
        list = []
        for key in conn.list_objects(Bucket=MY_BUCKET)['Contents']:
            list.append(key['Key'])
            print(list)
        desired_result = images
        self.assertListEqual(list, desired_result)


if __name__ == "__main__":
    unittest.main()
