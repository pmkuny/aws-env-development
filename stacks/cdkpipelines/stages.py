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
from stacks.infrastructure.monitoring import AmpStack

from stacks.cloud9.cloud9 import Cloud9EnvStack

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
        
        amp_stack = AmpStack(
            self,
            "AmpStack"
            )

class Cloud9EnvironmentStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cloud9_dev_env_stack = Cloud9EnvStack(self, "Cloud9DevEnvironment")

