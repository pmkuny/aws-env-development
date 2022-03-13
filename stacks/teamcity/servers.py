from aws_cdk import aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

class TeamCityEnterpriseServer(Stack):
    def __init__(self, scope: Construct, construct_id: str, my_networking_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.enterprise_sg = ec2.SecurityGroup(
            self,
            "TeamCityServerSecurityGroup",
            vpc=my_networking_stack.vpc,
            allow_all_outbound=True
        )

        self.instance = ec2.Instance(
            self,
            "TeamCityServerInstance",
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
            security_group=self.enterprise_sg,
            vpc=my_networking_stack.vpc,
        )

