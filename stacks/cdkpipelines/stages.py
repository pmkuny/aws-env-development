from multiprocessing import connection
import aws_cdk as cdk
import os
import logging
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from stacks.infrastructure.ecr import EcrStack
from stacks.infrastructure.eks_cluster import InfrastructureEksCluster
from stacks.infrastructure.networking import KubernetesNetworkingStack
from stacks.infrastructure.efs import ClusterFileSystemStack
from stacks.infrastructure.s3 import MyS3Stack

from stacks.teamcity.networking import TeamCityVpc
from stacks.teamcity.servers import TeamCityEnterpriseServer

class InfraStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network_stack = KubernetesNetworkingStack(
        self, 
        "KubernetesNetworkingStack", 
        my_cidr="10.40.0.0/16",
        )
    
        cluster_stack = InfrastructureEksCluster(
            self, 
            "InfrastructureEksCluster", 
            my_network_stack=network_stack, 
        )
    
        ecr_stack = EcrStack(
                self,
                "EcrStack",
        )

        efs_stack = ClusterFileSystemStack(
            self,
            "ClusterFilesystemStack",
            my_cluster_stack=cluster_stack,
            my_network_stack=network_stack
        )

        my_s3_stack = MyS3Stack(
            self,
            "MyS3Stack",
        )


class TeamCityStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.networking_stack = TeamCityVpc(self, "TeamCityVpcStack")
        self.server_stack = TeamCityEnterpriseServer(self, "TeamCityEnterpriseServerStack", my_networking_stack=self.networking_stack)