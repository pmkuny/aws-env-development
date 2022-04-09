import aws_cdk.aws_s3 as s3
from aws_cdk import Stack


from constructs import Construct

class MyS3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        my_bucket = s3.Bucket(self, "MyS3Bucket")