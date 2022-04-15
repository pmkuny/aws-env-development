from aws_cdk import Stack, App
import aws_cdk.assertions as assertions
from aws_cdk.assertions import Template, Match

from constructs import Construct

from stacks.teamcity.networking import *
from stacks.teamcity.servers import *

def test_teamcity_ports_present():
    app = App()
    
    # Dependency Stack
    networking_stack = TeamCityVpc(app, "TeamCityVpcStack")
    
    target_stack = TeamCityEnterpriseServer(app, "TeamCityEnterpriseServerStack", my_networking_stack=networking_stack)
    template = assertions.Template.from_stack(target_stack)
    
    # Test for Port 8111 (necessary for TeamCity)
    template.has_resource_properties(
        "AWS::EC2::SecurityGroup",
        {
            "SecurityGroupIngress": [
                {
                "CidrIp": Match.any_value(),
                "Description": Match.any_value(),
                "IpProtocol": Match.any_value(),
                "FromPort": 8111,
                "ToPort": 8111
                }
            ]
        })
        
    # Test for correct Instance Type
    template.has_resource_properties(
    "AWS::EC2::Instance",
    {
        "InstanceType": "t3.medium"
    }
        )