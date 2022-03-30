from multiprocessing import connection
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ssm as ssm
from stacks.helper_functions import *

class TeamCityEnterpriseServer(Stack):
    def __init__(self, scope: Construct, construct_id: str, my_networking_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define our user data for installing the TC binary
        self.tc_install = ec2.UserData.for_linux()
        self.tc_install.add_commands(
            "useradd -s /sbin/nologin -r -d /opt/TeamCity/ teamcity",
            "cd /opt/",
            "wget https://download.jetbrains.com/teamcity/TeamCity-2021.2.3.tar.gz",
            "tar xzvf TeamCity*",
            "rm -f TeamCity*.gz",
            "chown -R teamcity TeamCity/",
            "yum install -y java-1.8.0",
            "TeamCity/bin/runAll.sh start"
        )

        self.enterprise_sg = ec2.SecurityGroup(
            self,
            "TeamCityServerSecurityGroup",
            vpc=my_networking_stack.vpc,
            allow_all_outbound=True
        )

        # Add a rule allowing our IP to access the TeamCity UI
        self.enterprise_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(cidr_ip=get_ip(self)),
           connection=ec2.Port.tcp(8111),
        )

        self.instance = ec2.Instance(
            self,
            "TeamCityServerInstance",
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
            security_group=self.enterprise_sg,
            user_data=self.tc_install,
            user_data_causes_replacement=True,
            vpc=my_networking_stack.vpc,
        )

