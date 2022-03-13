import logging
import os
from ensurepip import version
from ossaudiodev import control_names
from platform import node
from select import select
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    Tags
)
from constructs import Construct
from stacks.infrastructure.networking import KubernetesNetworkingStack
import shortuuid

# Set default log level to warning, allowing override by Environment Variable
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)


class InfrastructureEksCluster(Stack):
    def __init__(self, scope: Construct, id: str, my_network_stack, **kwargs) -> None:
        super().__init__(scope, id)

        # List of subnets that can be passed into Cluster creation
        self.control_subnets = []
        self.worker_subnets = []

        # Select a Subnet Group based on name and return a list of ISubnet objects that are appeneded to a list to be passed to 
        # cluster creation later.
        for item in my_network_stack.kubernetes_vpc.select_subnets(subnet_group_name=my_network_stack.worker_subnets.name).subnets:
          self.worker_subnets.append(item)
        
        for item in my_network_stack.kubernetes_vpc.select_subnets(subnet_group_name=my_network_stack.control_subnets.name).subnets:
          self.control_subnets.append(item)

        # Built with most defaults in place
        # Security Groups and other related networking information are in the KubernetesNetworkingStack
        # We're setting default capacity here to 0 for managed nodegroups, because the only way we can specify the nodegroups be created in a specific subnet 
        # (the worker subnet) is by using the add_nodegroup_capacity method.
        self.cluster = eks.Cluster(
            self,
            "InfrastructureCluster",
            alb_controller=eks.AlbControllerOptions(version=eks.AlbControllerVersion.V2_3_1),
            default_capacity=0,
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            version=eks.KubernetesVersion.V1_21,
            security_group=my_network_stack.controlplane_security_group,
            vpc=my_network_stack.kubernetes_vpc,
            vpc_subnets=
            [
                 ec2.SubnetSelection(subnets=[*self.control_subnets]),
                 ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
            ],
        )

        self.worker_nodegroup = self.cluster.add_nodegroup_capacity(
            "WorkerNodeGroup",
            labels={"nodetype": "worker"},
            tags={
              "Name":f"EKS-{shortuuid.uuid()}"
            },
            subnets=ec2.SubnetSelection(subnets=[*self.worker_subnets])
        )

