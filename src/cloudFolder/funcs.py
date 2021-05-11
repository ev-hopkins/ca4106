import webbrowser
from botocore.exceptions import ClientError
import boto3


def uploadImages(images, MY_BUCKET):

    s3 = boto3.resource('s3')
    for image in images:
        data = open(image, 'rb')
        s3.Bucket(MY_BUCKET).put_object(Key=image,
                                                     Body=data,
                                                     ContentType='image/jpeg',
                                                     ContentDisposition='inline',
                                                     ACL='public-read',
                                                     ServerSideEncryption='AES256'
                                                     )
        print(data)


def createPresignedUrl(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name,
                                                            'ResponseContentType': 'image/jpeg'
                                                            },
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

