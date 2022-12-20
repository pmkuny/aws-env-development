from aws_cdk import aws_cloud9_alpha as c9
from aws_cdk import aws_ec2 as ec2

from constructs import Construct
from aws_cdk import Stack


class Cloud9EnvStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    
        vpc = ec2.Vpc(
            self,
            "VPC",
        )


        c9env = c9.Ec2Environment(
               self,
               "Cloud9Env",
               vpc=vpc,
               image_id=c9.ImageId.AMAZON_LINUX_2
               )
