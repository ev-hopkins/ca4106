import boto3
import webbrowser
from funcs import uploadImages, createPresignedUrl
import json


def main():
    client = boto3.client('s3')
    s3 = boto3.resource('s3')

    bucket_name = 'testbucketca4106'

    bucket = s3.Bucket('testbucketca4106')

    if not bucket.creation_date:
        response = client.create_bucket(
            Bucket='testbucketca4106',
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-1',
            },
        )


    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [
        {
            'Sid': 'AddPerm',
            'Effect': 'Deny',
            'Principal': '*',
            'Action': ['s3:GetObject', 
            ],
            'Resource': f'arn:aws:s3:::{bucket_name}/*',
            "Condition": {
                "StringNotLike": {
                    "aws:userId" : [
                        "AIDAVDMP3OANL3BUSXCMQ", #Dan
                        "AIDAVDMP3OANNS5H5EU3Z", #Tara
                        "AIDAVDMP3OANFRSXW7VF3", #Rhys
                        "AIDAVDMP3OANK72HWFQ7H", #Evan
                    ]
                }
            }
        },
        ]
    }

    bucket_policy = json.dumps(bucket_policy)

    s3 = boto3.client('s3')
    s3.put_bucket_policy(Bucket='testbucketca4106', Policy=bucket_policy)

    filelist = ['test0.jpg', 'test1.jpg', 'test2.jpg', 'test3.jpg', 'test4.jpg']

    uploadImages(filelist, 'testbucketca4106')


    for file in filelist:
        webbrowser.open(createPresignedUrl('testbucketca4106', file)) 
        
