import aws_cdk as cdk
from aws_cdk import aws_cloud9 as cloud9
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ssm as ssm

from constructs import Construct
from aws_cdk import Stack
from stacks.helper_functions import get_user_arn_from_iam, get_user_arn_from_ssm
from stacks.helper_functions import get_user_arn_from_ssm


class Cloud9EnvStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Calls a helper function to get the correct ARN for Cloud9 ownership
        current_arn = get_user_arn_from_ssm(self)
        print(current_arn)
    
        # Create our VPC to host our EC2 instance
        # Default Subnet Configurations here will give extra uneeded subnets.
        vpc = ec2.Vpc(
            self,
            "VPC",
        )
        
        # Create a Cloud9 instance that ties to our SSO-assumed role (taken from Parameter Store)
        self.dev_env = cloud9.CfnEnvironmentEC2(
            self,
            "DevEnvironment",
            automatic_stop_time_minutes=30,
            connection_type='CONNECT_SSM',
            description="Development Environment",
            image_id="amazonlinux-2-x86_64",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM).to_string(),
            name="Dev Environment",
            owner_arn=current_arn,
            subnet_id=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0]
            )
