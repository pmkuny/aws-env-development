from aws_cdk import aws_cloud9 as c9
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

        dev_env = c9.CfnEnvironmentEC2(
            self,
            "DevEnv",
            instance_type="m5.large",
            automatic_stop_time_minutes=60,
            connection_type="CONNECT_SSM",
            image_id="amazonlinux-2-x86_64",
            subnet_id=vpc.select_subnets(one_per_az=True).subnet_ids[0]
        )