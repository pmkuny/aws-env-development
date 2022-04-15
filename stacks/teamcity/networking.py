from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import Stack
from constructs import Construct


class TeamCityVpc(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "TeamCityVpc",
            cidr="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

        self.alb = elb.ApplicationLoadBalancer(
            self,
            "TeamCityServerAlb",
            internet_facing=True,
            vpc=self.vpc,
        )
